import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from patsy import dmatrices
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
import sqlalchemy as sql
import nfldb
db_config, paths_tried = nfldb.db.config()
if db_config is None:
    raise IOError("get_play_data: could not find database config! Looked"
                  " in these places: {0}".format(paths_tried))
db_config["drivername"] = "postgres"
db_config["username"] = db_config["user"]
del db_config["user"]
del db_config["timezone"]

engine = sql.create_engine(sql.engine.url.URL(**db_config))

def _make_nfldb_query_string(season_years=[2015], season_types=["Regular", "Postseason"]):

    where_clause = ("WHERE game.home_score != game.away_score "
                    "AND game.finished = TRUE")

    if season_years is not None:
        where_clause += " AND game.season_year"
        if len(season_years) == 1:
            where_clause += " = {0}".format(season_years[0])
        else:
            where_clause += (" in ({0})"
                             "".format(",".join([str(year) for year in season_years])))
    if season_types is not None:
        where_clause += " AND game.season_type"
        if len(season_types) == 1:
            where_clause += " = '{0}'".format(season_types[0])
        else:
            where_clause += " in ('{0}')".format("','".join(season_types))

    query_string = "SELECT "
    query_string += "passing_yds, rushing_yds, rushing_att, passing_sk_yds, receiving_yds, passing_att, passing_int, defense_int, fumbles_tot, penalty_yds, play_count, home_score, away_score, home_team, away_team, full_name"
    query_string += " FROM play_player"
    query_string += " INNER JOIN play on play_player.gsis_id = play.gsis_id"
    query_string += " INNER JOIN player on play_player.player_id = player.player_id"
    query_string += " INNER JOIN game on play_player.gsis_id = game.gsis_id"
    query_string += " INNER JOIN drive on play_player.gsis_id = drive.gsis_id"
    query_string += " " + where_clause
    query_string += " ORDER BY full_name LIMIT 99999;"

    return query_string

sql_string = _make_nfldb_query_string(season_years=[2015], season_types=["Regular", "Postseason"])

plays_df = pd.read_sql(sql_string, engine)

#We calculate who won the game based on the home score and away score
plays_df['team_won'] = np.where(plays_df.home_score > plays_df.away_score, 1, 0)



#Calculate Offensive Passing Rate = (offensive pass yds - sack yds) / pass plays
plays_df['off_pass_rate'] = (plays_df['passing_yds'] - plays_df['passing_sk_yds']) / (plays_df['passing_att'])
#Calculate Offensive Run Rate = offensive run yds / run plays
plays_df['off_run_rate'] = plays_df['rushing_yds'] / plays_df['rushing_att']
#Calculate Offensive Interception Rate = offensive interceptions / pass attempts
plays_df['off_int_rate'] = plays_df['passing_int'] / (plays_df['passing_att'])
#Calculate Offensive fumble Rate = fumbles / offensive plays
plays_df['off_fum_rate'] = plays_df['fumbles_tot'] / (plays_df['passing_att'] + plays_df['rushing_att'])
#Calculate Team Penalty Rate = team penalty yds / total plays
plays_df['team_pen_rate'] = plays_df['penalty_yds'] / (plays_df['play_count'])

#Replace all the statistical Nulls with 0's
plays_df['off_pass_rate'] = plays_df['off_pass_rate'].fillna(value=0).astype(np.int8)
plays_df['off_run_rate'] = plays_df['off_run_rate'].fillna(value=0).astype(np.int8)
plays_df['off_int_rate'] = plays_df['off_int_rate'].fillna(value=0).astype(np.int8)
plays_df['off_fum_rate'] = plays_df['off_fum_rate'].fillna(value=0).astype(np.int8)
plays_df['team_pen_rate'] = plays_df['team_pen_rate'].fillna(value=0).astype(np.int8)

#Keep only statistical categories for logistical regression
train_cols = plays_df.select_dtypes(exclude=['object'])

#Creating dataframe for classifier category "team_won" and calculated statistical categories
y, X = dmatrices('team_won ~ off_pass_rate + off_run_rate + off_int_rate + off_fum_rate + team_pen_rate', plays_df, return_type="dataframe")

#creating 1-D array
y = np.ravel(y)

# instantiate a logistic regression model, and fit with X and y
wins = LogisticRegression()

#Fit the logistic regression model
wins = wins.fit(X, y)

# check the accuracy on the training set
print wins.score(X, y)

#Split the examples in training(70%) and test sets(30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
wins2 = LogisticRegression()
wins2.fit(X_train, y_train)

#Predicted wins in the test set
predicted = wins2.predict(X_test)

#accuracy calculated on the test set
accuracy = accuracy_score(y_test,predicted)

print accuracy

