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
        homeAdvantage = 0
        awayAdvantage = 0
        homeTeam = (matchup.split(':')[0]).replace('LA', 'Los Angeles')
        awayTeam = (matchup.split(':')[1]).replace('LA', 'Los Angeles')
        homeGamesPlayed = (TeamStats(homeTeam))['games_played'][0]
        awayGamesPlayed = (TeamStats(awayTeam))['games_played'][0]
        
        if ((TeamStats(homeTeam))['assists'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['assists'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['points'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['points'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['field_goal_percentage'][0]) > ((TeamStats(awayTeam))['field_goal_percentage'][0]):
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['turnovers'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['turnovers'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['opp_points'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['opp_points'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['opp_field_goal_percentage'][0]) < ((TeamStats(awayTeam))['opp_field_goal_percentage'][0]):
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['opp_assists'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['opp_assists'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        print(homeTeam + ' has a ' + str(homeAdvantage) + ' point advantage over ' + awayTeam)
        print(awayTeam + ' has a ' + str(awayAdvantage) + ' point advantage over ' + homeTeam)
       

GameAnalysis()
