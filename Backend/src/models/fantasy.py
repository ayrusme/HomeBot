"""
This file contains all the models for Fantasy Premier League
"""
# TODO Use in-memory DB to host bootstrap-static data
# TODO Once the above todo is done, refactor top_player_common() logic with pandas

import grequests
import requests as req

OVERALL_LEAGUE_ID = 313
BOOTSTRAP = "https://fantasy.premierleague.com/drf/bootstrap-static"
GAMEWEEK_PICKS = "https://fantasy.premierleague.com/drf/entry/{TEAM_ID}/event/{GAMEWEEK}/picks"
ELEMENT_DETAIL = 'https://fantasy.premierleague.com/drf/element-summary/{ELEMENT_ID}'
LEAGUE_STANDINGS = 'https://fantasy.premierleague.com/drf/leagues-classic-standings/{LEAGUE_ID}'

BOOTSTRAP_STATIC = req.get(BOOTSTRAP)
BOOTSTRAP_STATIC = BOOTSTRAP_STATIC.json()


def get_current_gw():
    """
    Returns the current gameweek
    """
    return BOOTSTRAP_STATIC['current-event']


def get_next_gw():
    """
    Returns the next gameweek
    """
    return BOOTSTRAP_STATIC['next-event']


def get_player_by_id(idx):
    """
    Returns the player data by ID
    """
    return next((player for player in BOOTSTRAP_STATIC['elements'] if player['id'] == idx), None)


def most_transfer_in():
    """
    Returns the list of most transfered in players
    """
    # TODO Finish most transferred in players list
    pass


def no_change(team_id):
    """
    How many points would you have if you haven't changed 
    the team you had in Gameweek One
    """
    # TODO Write the logic for no_change()
    pass


def top_player_common():
    """
    A set of common players in the top 50 players' current team in the world
    """
    common_players = set()
    common_players_dict = {}
    response = req.get(LEAGUE_STANDINGS.format(LEAGUE_ID=OVERALL_LEAGUE_ID))
    current_gw = get_current_gw()
    player_data = set()
    for player in response.json()['standings']['results']:
        # Construct url for grequests
        player_data.add(grequests.get(GAMEWEEK_PICKS.format(
            TEAM_ID=player['id'], GAMEWEEK=current_gw)))
    # Make the requests and map
    responses = grequests.map(player_data)
    # Constuct final set
    count = 0
    for response in responses:
        if response.status_code == 200:
            count += 1
            for player in response.json()['picks']:
                player_info = get_player_by_id(player['element'])
                if player_info:
                    common_players.add(player_info['web_name'])
                    if player_info['web_name'] in common_players_dict:
                        common_players_dict[player_info['web_name']] += 1
                    else:
                        common_players_dict[player_info['web_name']] = 1
    # Sort dict
    print(sorted(common_players_dict.items(), key=lambda x: x[1], reverse=True))
    # print(len(responses), count)
    # print(common_players)


top_player_common()
