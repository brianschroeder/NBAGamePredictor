# Projects Plans for NBA Game Predictor
# Get All Games for the Day - Done
# Get Teams Stats for Home and Away Teams and put them in a Table - Done
# Compare teams FG%,PPG,FG% Defense,Assist,Turnovers

import requests
import json
import pandas as pd
from sportsreference.nba.teams import Teams

def nbaschedule():
    matchups = {}
    hometeams = []
    awayteams = [] 
    request = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').text
    request_json = json.loads(request)
    scoreboard = (request_json['scoreboard']['games'])
    for game in scoreboard:
        hometeams.append(game['homeTeam']['teamCity'] + ' ' + game['homeTeam']['teamName'])
        awayteams.append(game['awayTeam']['teamCity'] + ' ' + game['awayTeam']['teamName'])
    matchups.update({'Home Team': hometeams})
    matchups.update({'Away Team': awayteams})
    return matchups

def teamstats(teamname):
    teams = Teams()
    for team in teams: 
        df = pd.DataFrame(data=team.dataframe)
        stats = (df[['name', 'games_played', 'points', 'assists', 'turnovers', 'field_goal_percentage', 'rank', 'opp_points', 'opp_field_goal_percentage', 'opp_assists']])
        if stats.name[0] == teamname:
            return stats

print(nbaschedule())
     
