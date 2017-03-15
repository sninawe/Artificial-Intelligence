import pandas as pd
import numpy as np
import sqlalchemy as sql
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
#Query nfldb for fetching data where home_team wins
def _make_nfldb_query_string(season_years=None, season_types=None):

    offense_play_points = ("sum(play_player.fumbles_rec_tds * 6)+ "    # 6 points for fumble receiving touchdown
                           "sum(play_player.kicking_rec_tds * 6)+ "    # 6 points for kicking receiving touchdown
                           "sum(play_player.passing_tds * 6)+ "        # 6 points for passing touchdown
                           "sum(play_player.receiving_tds * 6)+ "       # 6 points for receiving touchdown
                           "sum(play_player.rushing_tds * 6)+ "         # 6 points for rushing touchdown
                           "sum(play_player.kicking_xpmade * 1)+ "      # 1 point for kicking
                           "sum(play_player.passing_twoptm * 2)+ "      # 2 points for passing 2 pointer
                           "sum(play_player.receiving_twoptm * 2)+ "    # 2 points for receiving 2 pointer
                           "sum(play_player.rushing_twoptm * 2)+ "     # 2 points for rushing 2 pointer
                           "sum(play_player.kicking_fgm * 3) "         # 3 points for kicking
                           "AS offense_play_points")
    defense_play_points = ("sum(play_player.defense_frec_tds * 6)+ "
                           "sum(play_player.defense_int_tds * 6)+ "
                           "sum(play_player.defense_misc_tds * 6)+ "
                           "sum(play_player.kickret_tds * 6)+ "
                           "sum(play_player.puntret_tds * 6)+ "
                           "sum(play_player.defense_safe * 2)+ "
                           "sum(play_player.defense_ast * 1)+ "
                           "sum(play_player.defense_fgblk * 1) "
                           "AS defense_play_points")


    where_clause = ("WHERE game.home_score != game.away_score "      # Where game is not a tie
# Game is finished
                    # home team has won the game
    #Player is in home_team
                    "AND game.finished = TRUE AND home_score > away_score AND full_name in (select full_name from player where away_team = team)")

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
    query_string += "full_name, home_team, away_team"
    query_string += ", " + offense_play_points
    query_string += ", " + defense_play_points
    query_string += " FROM play INNER JOIN play_player"
    query_string += (" ON play.gsis_id = play_player.gsis_id"
                 " AND play.drive_id = play_player.drive_id"
                 " AND play.play_id = play_player.play_id")
    query_string += " INNER JOIN game"
    query_string += " ON play.gsis_id = game.gsis_id"
    query_string += " INNER JOIN player"
    query_string += " ON play_player.player_id = player.player_id"
    query_string += " " + where_clause
    query_string += " GROUP BY full_name, home_team, away_team"
    query_string += " ORDER BY full_name, home_team, away_team;"

    return query_string

#Query nfldb for fetching data where away_team wins
def _make_nfldb_query_string1(season_years=None, season_types=None):

    offense_play_points = ("sum(play_player.fumbles_rec_tds * 6)+ "
                           "sum(play_player.kicking_rec_tds * 6)+ "
                           "sum(play_player.passing_tds * 6)+ "
                           "sum(play_player.receiving_tds * 6)+ "
                           "sum(play_player.rushing_tds * 6)+ "
                           "sum(play_player.kicking_xpmade * 1)+ "
                           "sum(play_player.passing_twoptm * 2)+ "
                           "sum(play_player.receiving_twoptm * 2)+ "
                           "sum(play_player.rushing_twoptm * 2)+ "
                           "sum(play_player.kicking_fgm * 3) "
                           "AS offense_play_points")
    defense_play_points = ("sum(play_player.defense_frec_tds * 6)+ "
                           "sum(play_player.defense_int_tds * 6)+ "
                           "sum(play_player.defense_misc_tds * 6)+ "
                           "sum(play_player.kickret_tds * 6)+ "
                           "sum(play_player.puntret_tds * 6)+ "
                           "sum(play_player.defense_safe * 2)+ "
                           "sum(play_player.defense_ast * 1)+ "
                           "sum(play_player.defense_fgblk * 1) "
                           "AS defense_play_points")


    where_clause = ("WHERE game.home_score != game.away_score "
                    "AND game.finished = TRUE AND away_score > home_score AND full_name in (select full_name from player where away_team = team)" )

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
    query_string += "full_name, home_team, away_team"
    query_string += ", " + offense_play_points
    query_string += ", " + defense_play_points
    query_string += " FROM play INNER JOIN play_player"
    query_string += (" ON play.gsis_id = play_player.gsis_id"
                     " AND play.drive_id = play_player.drive_id"
                     " AND play.play_id = play_player.play_id")
    query_string += " INNER JOIN game"
    query_string += " ON play.gsis_id = game.gsis_id"
    query_string += " INNER JOIN player"
    query_string += " ON play_player.player_id = player.player_id"
    query_string += " " + where_clause
    query_string += " GROUP BY full_name, home_team, away_team"
    query_string += " ORDER BY offense_play_points, defense_play_points;"

    return query_string
#Get data for 2015 Regular season where home_team wins
sql_string = _make_nfldb_query_string(season_years=[2015], season_types=["Regular"])
home_team_won = pd.read_sql(sql_string, engine)

#Get data for 20015 Regular season where away_team wins
sql_string1 = _make_nfldb_query_string1(season_years=[2015], season_types=["Regular"])
away_team_won = pd.read_sql(sql_string1, engine)

#Add offense play points and defense play points so that ranks can be created
home_team_won['total_points'] = home_team_won['offense_play_points'] + home_team_won['defense_play_points']
#Create Rank by total points grouped by each game(away_team and home_team are unnique in a season)
home_team_won['rank'] = home_team_won.groupby(["away_team", "home_team"])["total_points"].rank(method='min',ascending=False)
print home_team_won

#Add offense play points and defense play points so that ranks can be created
away_team_won['total_points'] = away_team_won['offense_play_points'] + away_team_won['defense_play_points']
#Create Rank by total points grouped by each game(away_team and home_team are unnique in a season)
away_team_won['rank'] = away_team_won.groupby(["away_team", "home_team"])["total_points"].rank(method='min',ascending=False)
print away_team_won