"""The Server file for Home Bot"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

import features

APP = Flask(__name__)
CORS(APP)

@APP.route("/", methods=['GET'])
def homepage():
    """Returns the homepage
    Returns
    ------
    homepage.html : html page
        contains information to be displated as the homepage

    """
    return render_template('homepage.html')

if __name__ == "__main__":
    APP.run(
        '0.0.0.0',
        8080,
        debug=True,
        threaded=True
        )
