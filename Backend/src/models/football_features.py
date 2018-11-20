"""Football Functions for the HomeBot"""

# TODO Rewrite everything in this file

import requests as reqs
from flask_table import Table, Col

PL_ENDPOINT = "http://api.football-data.org/v1/soccerseasons/445"
CURRENT_GW = "current"
ALL_GW = "all gameweeks"
RESULTS = "results"
SCHEDULED = "SCHEDULED"
TIMED = "TIMED"
FINISHED = "FINISHED"
LIVE = "IN_PLAY"


def get_response(league):
    if league == "PL":
        return reqs.get(PL_ENDPOINT)


def send_league_data():
    """
    API Function to get the teams in the league

    Returns
    -------
    table : list
        List of teams in the league
    """
    response = get_response("PL")
    teams = []
    if response.status_code == 200:
        # Sending the request to the leagueTable endpoint
        teams_list = reqs.get(response.json().get(
            '_links').get('teams').get('href'))
        for team in teams_list.json().get('teams'):
            teams.append({
                'name': team['name'],
                'crest': team['crestUrl']
            })
    return teams, response.status_code


def get_league_table():
    """
    API Function to get the league table

    Returns
    -------
    table : list
        list with the current football standings
        empty, if API fails
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
        # Sending the request to the leagueTable endpoint
        league_result = reqs.get(response.json().get(
            '_links').get('leagueTable').get('href'))
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
    return league_table, response.status_code


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
        # Sending the request to the fixtures endpoint
        fixtures_response = reqs.get(response.json().get(
            '_links').get('fixtures').get('href'))
        if response_indicator == CURRENT_GW:
            # Declaring the fixtures table
            class FixturesTable(Table):
                home_team = Col('Home Team')
                hiphen = Col('-')
                away_team = Col('Away Team')
                date = Col('Date & Time')
            for team in fixtures_response.json().get('fixtures'):
                if team['status'] == CURRENT_GW:
                    fixtures.append(dict(
                        # Ongoing feature
                    ))
