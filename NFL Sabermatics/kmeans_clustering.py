import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlalchemy as sql
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score
import nfldb
#Connect to nfldb using config file
db_config, paths_tried = nfldb.db.config()
if db_config is None:
    raise IOError("get_play_data: could not find database config! Looked"
                  " in these places: {0}".format(paths_tried))
db_config["drivername"] = "postgres"
db_config["username"] = db_config["user"]
del db_config["user"]
del db_config["timezone"]

engine = sql.create_engine(sql.engine.url.URL(**db_config))
#Query nfldb for fetching data
def _make_nfldb_query_string(season_years=[2015], season_types=["Regular", "Postseason"]):

    where_clause = ("WHERE game.home_score != game.away_score "
                    "AND game.finished = TRUE ")
# Where game is not a tie
# Game is finished

#Season year parameter
    if season_years is not None:
        where_clause += " AND game.season_year"
        if len(season_years) == 1:
            where_clause += " = {0}".format(season_years[0])
        else:
            where_clause += (" in ({0})"
                             "".format(",".join([str(year) for year in season_years])))
#Season type parameter
    if season_types is not None:
        where_clause += " AND game.season_type"
        if len(season_types) == 1:
            where_clause += " = '{0}'".format(season_types[0])
        else:
            where_clause += " in ('{0}')".format("','".join(season_types))
#Build Query
    query_string = "SELECT "
    query_string += "position, passing_yds, receiving_yds, kicking_fgmissed_yds, defense_ffum, defense_frec_yds, defense_int_yds, defense_fgblk, defense_misc_yds, defense_sk_yds, defense_tkl_loss_yds, fumbles_rec_yds, kicking_all_yds, kicking_fgm_yds, passing_sk_yds, full_name"
    query_string += " FROM play_player"
    query_string += " INNER JOIN player on play_player.player_id = player.player_id"
    query_string += " INNER JOIN game on play_player.gsis_id = game.gsis_id"
    query_string += " " + where_clause
    query_string += " ORDER BY full_name;"

    return query_string

#Get data for 2015 Regular season
sql_string = _make_nfldb_query_string(season_years=[2015], season_types=["Regular", "Postseason"])
df = pd.read_sql(sql_string, engine)

#Calculate mean for all the stats grouped by Full_name
plays = df.groupby(['full_name']).agg(np.mean)

#Create list for number of clusters
k = list(range(3,20))
scores = dict.fromkeys(k)
#Add stats to dataframe
data = scale(plays[['passing_yds', 'receiving_yds', 'kicking_fgmissed_yds', 'defense_ffum', 'defense_frec_yds', 'defense_int_yds', 'defense_fgblk', 'defense_misc_yds', 'defense_sk_yds', 'defense_tkl_loss_yds', 'fumbles_rec_yds', 'kicking_all_yds', 'kicking_fgm_yds', 'passing_sk_yds']].values)

#kmeans cluster fitting
for size in k:
    kmeans = KMeans(n_clusters=size)
    kmeans.fit(data)
    scores[size] = silhouette_score(data,kmeans.labels_)

#plot for silhouette score and cluster size
plt.plot(k,scores.values())
plt.title('K-means clustering of plays, 2015')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette score')
plt.show()
#3 clusters

#Applying kmeans clustering to the plays dataframe
kmeans = KMeans(n_clusters=3)
kmeans.fit(plays)

clusters = pd.DataFrame(kmeans.cluster_centers_,
                        columns=['passing_yds', 'receiving_yds', 'kicking_fgmissed_yds', 'defense_ffum', 'defense_frec_yds', 'defense_int_yds', 'defense_fgblk','defense_misc_yds', 'defense_sk_yds', 'defense_tkl_loss_yds', 'fumbles_rec_yds', 'kicking_all_yds', 'kicking_fgm_yds', 'passing_sk_yds'])

#creates unsupervised labels
plays['cluster']=kmeans.labels_

#print clusters

#Validation based on cluster values
player = plays[plays.cluster == 1]
player_table = player[player['passing_yds']>.2 ]
#print player_table

