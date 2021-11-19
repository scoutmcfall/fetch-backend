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


@app.route('/transaction', methods=["POST"])
def add_transaction():
    """Add transactions for a specific payer and date."""
    #getting a post request (from user or somewhere else)    
    input_json = request.get_json(force=True) 
    print(type(input_json))
    # if input_json is not list:
    #     input_json = [input_json]
    for transaction in input_json:
        payer = transaction["payer"]
        points = transaction["points"]
        timestamp = transaction["timestamp"]
        payer_var = session.get(payer,[])
        payer_var.append((points, timestamp))
        session[payer] = payer_var
    return ("", 200)


@app.route('/spend')
def spend_points(points):
    """Spend oldest (based on transaction timestamp) points first and return a list of 
    { "payer": <string>, "points": <integer> } for each call. 
    No payer's points should be negative.
    ex:
    [
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
    ]"""

    #get input from user
    #update session

@app.route('/balances')
def all_balances():
    """Return all payer point balances.
    {
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
    }"""

    #just prints session


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # app.run(debug=True)
    app.run(debug=True)

    

    test_data = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]
    
    res = requests.post('http://localhost:5000/transaction', json=test_data)

    print(res) #to see if request works
    print(res.data)