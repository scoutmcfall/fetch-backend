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

@app.route('/')
def homepage():
    """prepopulate session with test data"""
    test_data = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]



    for transaction in test_data:
        payer = transaction["payer"]
        points = transaction["points"]
        timestamp = transaction["timestamp"]
        payer_var = session.get(payer,[])
        payer_var.append({"points": points, "timestamp" : timestamp})
        session[payer] = payer_var

    ledger = []
    for transaction in test_data:
        ledger.append((timestamp, points, payer))
    session["ledger"] = ledger

    return ("", 200, )

@app.route('/transaction', methods=["GET"])
def add_transaction():
    """Add transactions for a specific payer and date. Update session and global ledger."""
    #getting a post request (from user or somewhere else)    
    transaction = request.args
    # print(type(input_json))
   
    payer = transaction["payer"]
    points = transaction["points"]
    timestamp = transaction["timestamp"]
    payer_var = session.get(payer,[])
    payer_var.append((timestamp, points ))
    session[payer] = payer_var

    session["ledger"].append((timestamp, points, payer))
   
    return ("", 200)


@app.route('/spend', methods=["GET"])
def spend_points():
    """
    Subtracts the point amount from the payer.
    Spend oldest (based on transaction timestamp) points first and return a list of 
    { "payer": <string>, "points": <integer> } for each call. 
    No payer's points should be negative.
    ex:
    [
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
    ]"""

    ledger = sorted(session["ledger"])
    spend = request.args
    cost = int(spend.get("points", 0))

    #sum up all points for all payers
    spending_limit = 0
    for timestamp, points, payer in ledger:
        spending_limit += points
    if cost <= spending_limit:
        remaining_total = spending_limit
        for timestamp, points, payer in ledger:
                payer_cost = min(remaining_total, points)
                remaining_total -= payer_cost
                # add transaction that subtracts minimum of remaining total and points
                request.get("/transaction", params = {"payer": payer, "points": -payer_cost, "timestamp": datetime.now() } )
                
    else:
        print("NO!")
    
    #we have to update session
      
        
     # will be a list of dictionaries formatted as "points", "timestamp"
    print(session)
    #so i should add a dictionary representing the subtraction
    #copy session dict into local dict
    # when points spent, deduct points from oldest to newest, until it's zero and then go to next one
    # then sum points and return them
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

  

