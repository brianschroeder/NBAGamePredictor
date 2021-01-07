# Projects Plans for NBA Game Predictor
# Get All Games for the Day - Done
# Get Teams Stats for Home and Away Teams and put them in a Table - Done
# Compare teams FG%,PPG,FG% Defense,Assist,Turnovers

import requests
import json
import pandas as pd
from sportsreference.nba.teams import Teams

def NbaSchedule():
    matchups = [] 
    request = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').text
    request_json = json.loads(request)
    scoreboard = (request_json['scoreboard']['games'])
    for game in scoreboard:
        matchups.append(game['homeTeam']['teamCity'] + ' ' + game['homeTeam']['teamName'] + ':' + game['awayTeam']['teamCity'] + ' ' + game['awayTeam']['teamName'])
    return matchups

def TeamStats(teamname):
    teams = Teams()
    for team in teams: 
        df = pd.DataFrame(data=team.dataframe)
        stats = (df[['name', 'games_played', 'points', 'assists', 'turnovers', 'field_goal_percentage', 'rank', 'opp_points', 'opp_field_goal_percentage', 'opp_assists']])
        if stats.name[0] == teamname:
            return stats

def GameAnalysis():
    for matchup in NbaSchedule():
        homeTeam = (matchup.split(':')[0]).replace('LA', 'Los Angeles')
        awayTeam = (matchup.split(':')[1]).replace('LA', 'Los Angeles')
        print(TeamStats(homeTeam))
        print(TeamStats(awayTeam))
