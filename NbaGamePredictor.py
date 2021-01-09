# Projects Plans for NBA Game Predictor
# Get All Games for the Day
# Get Teams Stats for Home and Away Teams and put them in a Table
# Compare teams FG%,PPG,FG% Defense,Assist,Turnovers

import requests
import json
import pandas as pd
from sportsreference.nba.teams import Teams
from bs4 import BeautifulSoup

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

def TeamRatings(teamname):
    RatingURL = 'https://www.basketball-reference.com/leagues/NBA_2021_ratings.html?sr&utm_source=direct&utm_medium=Share&utm_campaign=ShareTool#ratings'
    RatingResponse = requests.get(RatingURL)
    soup = BeautifulSoup(RatingResponse.content, 'html.parser')
    rating_columns = [  'Team','Conf', 'Div', 'W', 'L', 'W/L%', 'MOV', 'ORtg', 'DRtg', 'NRtg' , 'MOV/A',	'ORtg/A', 'DRtg/A', 'NRtg/A']
    df = pd.DataFrame(columns=rating_columns)
    rating_table = soup.find('table', attrs={'class': 'sortable stats_table', 'id':'ratings'}).tbody
    trs = rating_table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        row = [td.text.replace('\n', '') for td in tds]
        df = df.append(pd.Series(row, index=rating_columns), ignore_index=True)
    team_filtered = (df.query('Team == @teamname'))
    team_rating = (team_filtered[['Team', 'MOV/A',	'ORtg/A', 'DRtg/A']])
    return(team_rating)

def GameAnalysis():
    all_stats = []
    for matchup in NbaSchedule():
        homeAdvantage = 0
        awayAdvantage = 0
        homeTeam = (matchup.split(':')[0]).replace('LA', 'Los Angeles')
        awayTeam = (matchup.split(':')[1]).replace('LA', 'Los Angeles')
        homeGamesPlayed = (TeamStats(homeTeam))['games_played'][0]
        awayGamesPlayed = (TeamStats(awayTeam))['games_played'][0]
    
        if ((TeamStats(homeTeam))['points'][0])/homeGamesPlayed > ((TeamStats(homeTeam))['opp_points'][0])/homeGamesPlayed:
            homeAdvantage += 4
        
        if ((TeamStats(awayTeam))['points'][0])/awayGamesPlayed > ((TeamStats(awayTeam))['opp_points'][0])/awayGamesPlayed:
            awayAdvantage += 4
        
        if ((TeamStats(homeTeam))['assists'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['assists'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['points'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['points'][0])/awayGamesPlayed:
            homeAdvantage += 2
        else: 
            awayAdvantage += 2
        if ((TeamStats(homeTeam))['field_goal_percentage'][0]) > ((TeamStats(awayTeam))['field_goal_percentage'][0]):
            homeAdvantage += 3
        else: 
            awayAdvantage += 3
        if ((TeamStats(homeTeam))['turnovers'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['turnovers'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        if ((TeamStats(homeTeam))['opp_points'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['opp_points'][0])/awayGamesPlayed:
            homeAdvantage += 2
        else: 
            awayAdvantage += 2
        if ((TeamStats(homeTeam))['opp_field_goal_percentage'][0]) < ((TeamStats(awayTeam))['opp_field_goal_percentage'][0]):
            homeAdvantage += 3
        else: 
            awayAdvantage += 3
        if ((TeamStats(homeTeam))['opp_assists'][0])/homeGamesPlayed < ((TeamStats(awayTeam))['opp_assists'][0])/awayGamesPlayed:
            homeAdvantage += 1
        else: 
            awayAdvantage += 1
        #print(homeTeam + ' has a ' + str(homeAdvantage) + ' point advantage over ' + awayTeam)
        #print(awayTeam + ' has a ' + str(awayAdvantage) + ' point advantage over ' + homeTeam)

        stats = {
            'Home Team': homeTeam,
            'Home PPG': ((TeamStats(homeTeam))['points'][0])/homeGamesPlayed,
            'Home Assists P/G' : ((TeamStats(homeTeam))['assists'][0])/homeGamesPlayed,
            'Home FG%': ((TeamStats(homeTeam))['field_goal_percentage'][0]),
            'Home Turnovers P/G': ((TeamStats(homeTeam))['turnovers'][0])/homeGamesPlayed, 
            'Home Allowed PPG': ((TeamStats(homeTeam))['opp_points'][0])/homeGamesPlayed,
            'Home Allowed FG%': ((TeamStats(homeTeam))['opp_field_goal_percentage'][0]),
            'Home Allowed Assist P/G': ((TeamStats(homeTeam))['opp_assists'][0])/homeGamesPlayed,
            'Away Team': awayTeam,
            'Away PPG': ((TeamStats(awayTeam))['points'][0])/awayGamesPlayed,
            'Away Assists P/G' : ((TeamStats(awayTeam))['assists'][0])/awayGamesPlayed,
            'Away FG%': ((TeamStats(awayTeam))['field_goal_percentage'][0]),
            'Away Turnovers P/G': ((TeamStats(awayTeam))['turnovers'][0])/awayGamesPlayed, 
            'Away Allowed PPG': ((TeamStats(awayTeam))['opp_points'][0])/awayGamesPlayed,
            'Away Allowed FG%': ((TeamStats(awayTeam))['opp_field_goal_percentage'][0]),
            'Away Allowed Assist P/G': ((TeamStats(awayTeam))['opp_assists'][0])/awayGamesPlayed,
            'Home Team Advantage': homeAdvantage,
            'Away Team Advantage': awayAdvantage,
            'Home Team Defensive Rating' : (TeamRatings(homeTeam)['DRtg/A'].to_string()).split('   ')[1],
            'Away Team Defensive Rating' : (TeamRatings(awayTeam)['DRtg/A'].to_string()).split('   ')[1],
            'Home Team Ofensive Rating' : (TeamRatings(homeTeam)['ORtg/A'].to_string()).split('   ')[1],
            'Away Team Ofensive Rating' : (TeamRatings(awayTeam)['ORtg/A'].to_string()).split('   ')[1],
            'Home Team MOV/A' : (TeamRatings(homeTeam)['MOV/A'].to_string()).split('   ')[1],
            'Away Team MOV/A' : (TeamRatings(awayTeam)['MOV/A'].to_string()).split('   ')[1]
        }

        all_stats.append(stats)
    stats_dataframe = pd.DataFrame(data = all_stats)
    stats_dataframe_sorted = stats_dataframe.sort_values(by='Home Team Advantage', ascending=False)
    html = stats_dataframe_sorted.to_html(classes='table table-striped table-hover')
    html_file = open("index.html", "w")
    html_file.write(html)
    html_file.close()

GameAnalysis()
