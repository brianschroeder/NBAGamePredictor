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
        stats = (df[['name', 'games_played', 'points', 'assists', 'turnovers', 'field_goal_percentage', 'rank', 'opp_points', 'opp_field_goal_percentage', 'opp_assists', 'field_goal_attempts', 'total_rebounds', 'three_point_field_goal_percentage']])
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
        home_assist_turnover_ratio = (((TeamStats(homeTeam))['assists'][0])/homeGamesPlayed)/(((TeamStats(homeTeam))['turnovers'][0])/homeGamesPlayed)
        away_assist_turnover_ratio = (((TeamStats(awayTeam))['assists'][0])/awayGamesPlayed)/(((TeamStats(awayTeam))['turnovers'][0])/awayGamesPlayed)

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

        if home_assist_turnover_ratio > away_assist_turnover_ratio:
            home_at_advantage = home_assist_turnover_ratio - away_assist_turnover_ratio
            away_at_advantage = away_assist_turnover_ratio - home_assist_turnover_ratio
        else:
            away_at_advantage = away_assist_turnover_ratio - home_assist_turnover_ratio
            home_at_advantage = home_assist_turnover_ratio - away_assist_turnover_ratio

        if ((TeamStats(homeTeam))['total_rebounds'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['total_rebounds'][0])/awayGamesPlayed:
            home_rb_advantage = ((TeamStats(homeTeam))['total_rebounds'][0])/homeGamesPlayed - ((TeamStats(awayTeam))['total_rebounds'][0])/awayGamesPlayed
            away_rb_advantage = ((TeamStats(awayTeam))['total_rebounds'][0])/awayGamesPlayed - ((TeamStats(homeTeam))['total_rebounds'][0])/homeGamesPlayed
        else:
            away_rb_advantage = ((TeamStats(awayTeam))['total_rebounds'][0])/awayGamesPlayed - ((TeamStats(homeTeam))['total_rebounds'][0])/homeGamesPlayed
            home_rb_advantage = ((TeamStats(homeTeam))['total_rebounds'][0])/homeGamesPlayed - ((TeamStats(awayTeam))['total_rebounds'][0])/awayGamesPlayed
        
        if ((TeamStats(homeTeam))['three_point_field_goal_percentage'][0]) > ((TeamStats(awayTeam))['three_point_field_goal_percentage'][0]):
            home_three_advantage = ((TeamStats(homeTeam))['three_point_field_goal_percentage'][0]) - ((TeamStats(awayTeam))['three_point_field_goal_percentage'][0])
            away_three_advantage = ((TeamStats(awayTeam))['three_point_field_goal_percentage'][0]) - ((TeamStats(homeTeam))['three_point_field_goal_percentage'][0])
        else:
            away_three_advantage = ((TeamStats(awayTeam))['three_point_field_goal_percentage'][0]) - ((TeamStats(homeTeam))['three_point_field_goal_percentage'][0])
            home_three_advantage = ((TeamStats(homeTeam))['three_point_field_goal_percentage'][0]) - ((TeamStats(awayTeam))['three_point_field_goal_percentage'][0])

        if ((TeamStats(homeTeam))['field_goal_percentage'][0]) > ((TeamStats(awayTeam))['field_goal_percentage'][0]):
            home_fg_advantage = ((TeamStats(homeTeam))['field_goal_percentage'][0]) - ((TeamStats(awayTeam))['field_goal_percentage'][0])
            away_fg_advantage = ((TeamStats(awayTeam))['field_goal_percentage'][0]) - ((TeamStats(homeTeam))['field_goal_percentage'][0])
        else:
            away_fg_advantage = ((TeamStats(awayTeam))['field_goal_percentage'][0]) - ((TeamStats(homeTeam))['field_goal_percentage'][0])
            home_fg_advantage = ((TeamStats(homeTeam))['field_goal_percentage'][0]) - ((TeamStats(awayTeam))['field_goal_percentage'][0])
        
        if ((TeamStats(homeTeam))['field_goal_attempts'][0])/homeGamesPlayed > ((TeamStats(awayTeam))['field_goal_attempts'][0])/awayGamesPlayed:
            home_fga_advantage = ((TeamStats(homeTeam))['field_goal_attempts'][0])/homeGamesPlayed - ((TeamStats(awayTeam))['field_goal_attempts'][0])/awayGamesPlayed
            away_fga_advantage = ((TeamStats(awayTeam))['field_goal_attempts'][0])/awayGamesPlayed - ((TeamStats(homeTeam))['field_goal_attempts'][0])/homeGamesPlayed
        else:
            away_fga_advantage = ((TeamStats(awayTeam))['field_goal_attempts'][0])/awayGamesPlayed - ((TeamStats(homeTeam))['field_goal_attempts'][0])/homeGamesPlayed
            home_fga_advantage = ((TeamStats(homeTeam))['field_goal_attempts'][0])/homeGamesPlayed - ((TeamStats(awayTeam))['field_goal_attempts'][0])/awayGamesPlayed

        stats = {
            'Home Team': homeTeam,
            'Away Team': awayTeam,
            'Home Defensive Rating Difference': home_dr_advantage,
            'Away Defensive Rating Difference': away_dr_advantage,
            'Home Offensive Rating Difference': home_or_advantage,
            'Away Offensive Rating Difference': away_or_advantage,
            'Home Rebound Advantage': home_rb_advantage,
            'Away Rebound Advantage' : away_rb_advantage,
            'Home Three Point Advantage': home_three_advantage,
            'Away Three Point Advantage': away_three_advantage,
            'Home FG% Difference': home_fg_advantage,
            'Away FG% Difference': away_fg_advantage,
            'Home Assists/Turnover Ratio Difference' : home_at_advantage,
            'Away Assists/Turnover Ratio Difference' : away_at_advantage,
            'Home FGA Difference': home_fga_advantage,
            'Away FGA Difference': away_fga_advantage,
        }

        all_stats.append(stats)
    stats_dataframe = pd.DataFrame(data = all_stats)
    stats_dataframe_sorted = stats_dataframe.sort_values(by='Home Team Advantage', ascending=False)
    stats_dataframe_sorted.to_html('/var/www/html/index.html')
GameAnalysis()
