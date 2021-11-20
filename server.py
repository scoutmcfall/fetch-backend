"""Server for Fetch Rewards application"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

import os
import requests
from jinja2 import StrictUndefined
from datetime import date, timedelta, datetime
import json

app = Flask(__name__)

app.secret_key = "dev" 
app.jinja_env.undefined = StrictUndefined

# API_KEY = os.environ["API_KEY"]


@app.route('/transaction', methods=["GET"])
def add_transaction():
    """Add transactions for a specific payer and date."""
    #getting a post request (from user or somewhere else)    
    input_json = request.args
    print(type(input_json))
    if input_json is not list:
        input_json = [input_json]
    for transaction in input_json:
        payer = transaction["payer"]
        points = transaction["points"]
        timestamp = transaction["timestamp"]
        payer_var = session.get(payer,[])
        payer_var.append({"points": points, "timestamp" : timestamp})
        session[payer] = payer_var
    # Now my session looks like this: 
    # <SecureCookieSession {'DANNON': [{'points': 1000, 'timestamp': '2020-11-02T14:00:00Z'}, 
    # {'points': -200, 'timestamp': '2020-10-31T15:00:00Z'}, 
    # {'points': 300, 'timestamp': '2020-10-31T10:00:00Z'}], 
    # 'UNILEVER': [{'points': 200, 'timestamp': '2020-10-31T11:00:00Z'}], 
    # 'MILLER COORS': [{'points': 10000, 'timestamp': '2020-11-01T14:00:00Z'}]}>
    print(session)
    return ("", 200)


@app.route('/spend', methods=["GET"])
def spend_points():
    """Subtracts the point amount from the payer.
    Spend oldest (based on transaction timestamp) points first and return a list of 
    { "payer": <string>, "points": <integer> } for each call. 
    No payer's points should be negative.
    ex:
    [
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
    ]"""
    input_json = request.args
    print(input_json, type(input_json))
    payer = input_json.get("payer", "")
    points = int(input_json.get("points", 0))
    print(session)
    session[payer].append({"points": -points, "timestamp": datetime.now() }) # will be a list of dictionaries formatted as "points", "timestamp"
    print(session)
    #so i should add a dictionary representing the subtraction
    return("", 200)

@app.route('/balances', methods=["POST"])
def all_balances():
    """Return all payer point balances. If negative, reset to 0.
    {
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
    }"""
    points_dict = {}
    for payer in session:
        points_dict[payer] = [session[payer]["points"]]
        if sum(points_dict[payer]) < 0:
            points_dict[payer] = 0
    return points_dict


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # app.run(debug=True)
    app.run(debug=True)

  

