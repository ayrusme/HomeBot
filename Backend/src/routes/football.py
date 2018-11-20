"""
Routes for the football models
"""

from flask import Blueprint, render_template, jsonify
from .. import codes
from ..models import football_features as football

FOOTBALL = Blueprint('football', __name__, url_prefix='/football')


@FOOTBALL.route("/PL/")
def send_league_data():
    return jsonify(football.send_league_data())


@FOOTBALL.route("/PL/leaguetable/")
def get_league_table():
    return jsonify(football.get_league_table())


@FOOTBALL.route("/PL/fixtures")
def get_fixtures():
    return jsonify(football.get_league_fixtures(codes.CURRENT_GW))
