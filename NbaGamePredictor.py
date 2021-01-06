# Projects Plans for NBA Game Predictor
# Get All Games for the Day
# Get Teams Stats for Home and Away Teams and put them in a Table
# Compare teams FG%,PPG,FG% Defense,Assist,Turnovers

import requests
import json
import pandas as pd
hometeam = []
hometeamwins = []
hometeamlosses = []
awayteam = []
awayteamwins = []
awayteamlosses = []
todaysgames = {}
request = requests.get('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json').text
request_json = json.loads(request)
scoreboard = (request_json['scoreboard']['games'])
for game in scoreboard:
    #dailygames.update({ 'Home Team' : game })
    hometeam.append(game['homeTeam']['teamName'])
    awayteam.append(game['awayTeam']['teamName'])
    hometeamwins.append(game['homeTeam']['wins'])
    awayteamwins.append(game['awayTeam']['wins'])
    hometeamlosses.append(game['homeTeam']['losses'])
    awayteamlosses.append(game['awayTeam']['losses'])

todaysgames.update({'Home Team': hometeam})
todaysgames.update({'Home Team Wins': hometeamwins})
todaysgames.update({'Home Team Losses': hometeamlosses})
todaysgames.update({'Away Team': awayteam})
todaysgames.update({'Away Team Wins': awayteamwins})
todaysgames.update({'Away Team Losses': awayteamlosses})

df = pd.DataFrame(data=todaysgames)

print(df)
