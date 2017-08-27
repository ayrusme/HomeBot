"""The Server file for Home Bot"""

from flask import Flask, jsonify, render_template, request

import codes
import football_features as football

APP = Flask(__name__)

@APP.route("/", methods=['GET'])
def homepage():
    """Returns the homepage
    Returns
    ------
    homepage.html : html page
        contains information to be displated as the homepage

    """
    return render_template('homepage.html')

@APP.route("/football/")
def send_available_endpoints():
    return ("""
              /football/PL/ : For information about Premier League &nbsp
              /football/PL/leaguetable/ : For the current Premier League table &nbsp
              /football/PL/fixtures/ : For current GW fixtures &nbsp
              /football/PL/fixtures/all/ : For fixtures for all GW's &nbsp
              /football/PL/results/ : For results in the current season &nbsp
              /football/PL/live/ : For live match scores   
            """)

@APP.route("/football/PL/")
def send_league_data():
    return football.send_league_data()

@APP.route("/football/PL/leaguetable/")
def get_league_table():
    return football.get_league_table()

@APP.route("/football/PL/fixtures")
def get_fixtures():
    return football.get_league_fixtures(codes.CURRENT_GW)

if __name__ == "__main__":
    APP.run(
        '0.0.0.0',
        8080,
        debug=True,
        threaded=True
        )
