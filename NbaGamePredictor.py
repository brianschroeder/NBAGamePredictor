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
        homeTeam = (matchup.split(':')[0]).replace('LA', 'Los Angeles')
        awayTeam = (matchup.split(':')[1]).replace('LA', 'Los Angeles')
        homeGamesPlayed = (TeamStats(homeTeam))['games_played'][0]
        awayGamesPlayed = (TeamStats(awayTeam))['games_played'][0]
        home_defense_rating = float((TeamRatings(homeTeam)['DRtg/A'].to_string()).split('   ')[1])
        away_defense_rating = float((TeamRatings(awayTeam)['DRtg/A'].to_string()).split('   ')[1])
        home_offense_rating = float((TeamRatings(homeTeam)['ORtg/A'].to_string()).split('   ')[1])
        away_offense_rating = float((TeamRatings(awayTeam)['ORtg/A'].to_string()).split('   ')[1])
    
        if home_defense_rating < away_defense_rating:
            home_dr_advantage = away_defense_rating - home_defense_rating 
            away_dr_advantage = home_defense_rating - away_defense_rating 
        else:
            away_dr_advantage = home_defense_rating - away_defense_rating
            home_dr_advantage = away_defense_rating - home_defense_rating 
        
        if home_offense_rating > away_offense_rating:
            home_or_advantage = home_offense_rating - away_offense_rating
            away_or_advantage = away_offense_rating - home_offense_rating
        else:
            away_or_advantage = away_offense_rating - home_offense_rating
            home_or_advantage = home_offense_rating - away_offense_rating
        stats = {
            'Home Team': homeTeam,
            'Away Team': awayTeam,
            'Home Team Defensive Rating Difference': home_dr_advantage,
            'Away Team Defensive Rating Difference': away_dr_advantage,
            'Home Team Offensive Rating Difference': home_or_advantage,
            'Away Team Offensive Rating Difference': away_or_advantage,
            'Home FG%': ((TeamStats(homeTeam))['field_goal_percentage'][0]),
            'Away FG%': ((TeamStats(awayTeam))['field_goal_percentage'][0]),
            'Home Assists P/G' : ((TeamStats(homeTeam))['assists'][0])/homeGamesPlayed,
            'Away Assists P/G' : ((TeamStats(awayTeam))['assists'][0])/awayGamesPlayed,
            'Home Turnovers P/G': ((TeamStats(homeTeam))['turnovers'][0])/homeGamesPlayed,
            'Away Turnovers P/G': ((TeamStats(awayTeam))['turnovers'][0])/awayGamesPlayed
        }

        all_stats.append(stats)
    stats_dataframe = pd.DataFrame(data = all_stats)
    html = stats_dataframe.to_html(classes='table table-striped table-hover')
    html_file = open("index.html", "w")
    html_file.write(html)
    html_file.close()

GameAnalysis()
