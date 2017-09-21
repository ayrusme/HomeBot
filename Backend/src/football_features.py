"""Football Functions for the HomeBot"""

import requests as reqs
from flask_table import Table, Col

import codes

def get_response(league):
    if league == "PL":
        return reqs.get(codes.PL_ENDPOINT)


def send_league_data():
    """
    API Function to get the teams in the league

    Returns
    -------
    table.__html__() : table
        HTML table with the teams in a league
    """
    response = get_response("PL")
    if response.status_code == 200:
        # Declaring the teams table
        class TeamsTable(Table):
            name = Col('Team Name')
            crest = Col('Crest')
        # Sending the request to the leagueTable endpoint
        teams = []
        teams_list = reqs.get(response.json().get('_links').get('teams').get('href'))
        
        for team in teams_list.json().get('teams'):
            teams.append(dict(
                name = team['name'],
                # crest="<img src=\"" + team['crestUrl'] + "\"/>"
                crest = team['crestUrl']
            ))
        # Populate the table
        #table = TeamsTable(teams)
        # Return the html
        #return table.__html__()
        return teams

def get_league_table():
    """
    API Function to get the league table

    Returns
    -------
    table.__html__() : table
        HTML table with the current football standings
    None : none
        NoneType Object since the calling API didn't send any response
    """
    league_table = []
    response = get_response("PL")
    if response.status_code == 200:
        # Declaring the football table
        class LeagueTable(Table):
            pos = Col('#')
            team = Col('Team')
            played = Col('MP')
            won = Col('W')
            draw = Col('D')
            lost = Col('L')
            goals_scored = Col('GF')
            goals_conc = Col('GC')
            goal_diff = Col("GD")
            points = Col('P')
        #Sending the request to the leagueTable endpoint
        league_result = reqs.get(response.json().get('_links').get('leagueTable').get('href'))
        for team in league_result.json().get('standing'):
            league_table.append(dict(
                pos=team['position'],
                team=team['teamName'],
                played=team['playedGames'],
                won=team['wins'],
                draw=team['draws'],
                lost=team['losses'],
                goals_scored=team['goals'],
                goals_conc=team['goalsAgainst'],
                goal_diff=team['goalDifference'],
                points=team['points']
            ))
        # Populate the table
        table = LeagueTable(league_table)
        # Return the html
        return table.__html__()
    else:
        return None, 503

def get_league_fixtures(response_indicator):
    """
    API Function to get the league fixtures
    
    Parameters
    -------
    response_indicator : string
        Specifies if the fixtures are needed for the entire gameweek or the current gameweek
    
    Returns
    -------

    """
    response = get_response("PL")
    current_match_week = response.json().get('currentMatchday')
    if response.status_code == 200:
        fixtures = []
        #Sending the request to the fixtures endpoint
        fixtures_response = reqs.get(response.json().get('_links').get('fixtures').get('href'))
        if response_indicator == codes.CURRENT_GW:
            # Declaring the fixtures table
            class FixturesTable(Table):
                home_team = Col('Home Team')
                hiphen = Col('-')
                away_team = Col('Away Team')
                date = Col('Date & Time')
            for team in fixtures_response.json().get('fixtures'):
                if team['status'] == codes.CURRENT_GW:
                    fixtures.append(dict(
                        #Ongoing feature                        
                    ))
