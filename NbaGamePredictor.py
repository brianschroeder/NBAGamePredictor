# Projects Plans for NBA Game Predictor
# Get All Games for the Day - Done
# Get Teams Stats for Home and Away Teams and put them in a Table
# Compare teams FG%,PPG,FG% Defense,Assist,Turnovers

import requests
import json
import pandas as pd

def nbaschedule(showschedule):
    hometeam = []
    hometeamID = []
    hometeamwins = []
    hometeamlosses = []
    awayteam = []
    awayteamID = []
    awayteamwins = []
    awayteamlosses = []
    todaysgames = {}
    teamIDs = {} 
    request = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').text
    request_json = json.loads(request)
    scoreboard = (request_json['scoreboard']['games'])
    for game in scoreboard:
        hometeam.append(game['homeTeam']['teamName'])
        awayteam.append(game['awayTeam']['teamName'])
        hometeamwins.append(game['homeTeam']['wins'])
        awayteamwins.append(game['awayTeam']['wins'])
        hometeamlosses.append(game['homeTeam']['losses'])
        awayteamlosses.append(game['awayTeam']['losses'])
        hometeamID.append(game['homeTeam']['teamId'])
        awayteamID.append(game['awayTeam']['teamId'])
    todaysgames.update({'Home Team': hometeam})
    todaysgames.update({'Home Team Wins': hometeamwins})
    todaysgames.update({'Home Team Losses': hometeamlosses})
    todaysgames.update({'Away Team': awayteam})
    todaysgames.update({'Away Team Wins': awayteamwins})
    todaysgames.update({'Away Team Losses': awayteamlosses})
    teamIDs.update({'Home Team ID': hometeamID})
    teamIDs.update({'Away Team ID': awayteamID})
    df = pd.DataFrame(data=todaysgames)
    if showschedule == True:
        print(df.sort_values(by=['Home Team Wins'], ascending=False))
    return teamIDs


def teamstats():
    request = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').text
    request_json = json.loads(request)
    scoreboard = (request_json['scoreboard']['games'])
    for game in scoreboard:
        print(game['homeTeam']['teamId'])
        print(game['awayTeam']['teamId'])
        print('New Game')
teamstats()
