"""The Server file for Home Bot"""

from flask import Flask, jsonify, render_template, request

import codes
import football_features as football

APP = Flask(__name__)


if __name__ == "__main__":
    APP.run(
        '0.0.0.0',
        8080,
        debug=True,
        threaded=True
        )
