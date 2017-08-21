"""Functions for the HomeBot"""
import requests as reqs

import codes

def get_league_table():
    """API Function to get the league table
    Returns
    -------
    
    """
    league_table = []
    response = reqs.get(codes.PL_ENDPOINT)
    if response.status_code == 200:
        league_endpoint = response.json().get('leagueTable')
        league_result = reqs.get(league_endpoint)
        