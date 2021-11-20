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






"""
each transaction is read in individually and the list of positive transactions is stored in session as ledger
if it is positive, it's added to the end of ledger (a list of dictionaries)
if it's negative, it's added to negs (list of dictionaries) which the spend route iterates through, 
subtracting each from ledger and updating ledger each iteration 

so, session consists of: {ledger: [], negs: [], payer_totals:{}}

in order to return the totals/payer, iterate through the updated ledger and populate a dictionary of {payer:points}
using .get
then return that dictionary
"""



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
        if transaction["points"] > 0:
            # payer_var = session.get(payer,[])
            # payer_var.append({"points": points, "timestamp" : timestamp})
            # session[payer] = payer_var
            ledger = session.get("ledger", [])
            ledger.append((timestamp, points, payer))
            session["ledger"] = ledger
        else:
            negs = session.get("negs", [])
            negs.append((timestamp, points, payer))
            session["negs"] = negs
            #now the list of negative transations can be processed in the spend route against the postive transactions in ledger
    print(session["ledger"])
    print(session["negs"])
    return ("", 200, )

@app.route('/transaction', methods=["GET"])
def add_transaction(payer = "", points = "", timestamp = ""):
    """Add positive or negative transactions to correct lists for 
    a specific payer and date. Update session, global ledger, global negs."""
    transaction = request.args
    if not payer:
        payer = transaction["payer"]
    if not points:
        points = transaction["points"]
    if not timestamp:
        timestamp = transaction["timestamp"]
    if int(transaction["points"]) > 0:
            payer = transaction["payer"]
            points = transaction["points"]
            timestamp = transaction["timestamp"]
            ledger = session.get("ledger", [])
            ledger.append((timestamp, points, payer))
            # session["ledger"] = ledger
    else:
        negs = session.get("negs", [])
        negs.append((timestamp, points, payer))
        # session["negs"] = negs
    
   
    # payer_var = session.get(payer,[])
    # payer_var.append((timestamp, points))
    # session[payer] = payer_var

    # session["ledger"].append((timestamp, points, payer))
   
    return ("", 200)


@app.route('/spend', methods=["GET"])
def spend_points(cost):
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
    # print(session["ledger"])
    # ledger = sorted(session["ledger"][:])
  
    negs = session["negs"]
    ledger = sorted(session["ledger"])
    spend = request.args
    if not cost:
        cost = spend
    cost = int(spend.get("points", 0))

    for timestamp, points, payer in negs:
        cost += int(points) 
    
    #sum up all points for all payers
    spending_limit = 0
    print(ledger)
    print(negs)
    for transaction in ledger:
        points = transaction[1]
        spending_limit += points
    if cost <= spending_limit:
        remaining_total = spending_limit
        for timestamp, points, payer in ledger:
            if remaining_total == 0:
                break
            else:
                payer_cost = min(remaining_total, points)
                remaining_total -= payer_cost
                spend_points(payer_cost)
                # add transaction that subtracts minimum of remaining total and points
                # add_transaction(payer = payer, points = -payer_cost, timestamp = str(datetime.now()))
                #but what we want to do is restart this spend loop, so i should call spend_points() on remaining payer cost?
                
                
    else:
        print("NO!")
    #clear negs list after processing them all against the ledger
    session["negs"] = []
    print("aaaaaaaaaaaaaahahahahahah")
    print(session["ledger"])
    print(session["negs"])

    return("", 200)

@app.route('/balances', methods=["POST"])
def all_balances():
    """Return all payer point balances. If negative, reset to 0.
    {
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
    }"""
    balance = {}
    for timestamp, points, payer in ledger:
        balance[payer] = session.get(payer, [])
    print(balance)


    
    # points_dict = {}
    # for payer in session:
    #     points_dict[payer] = [session[payer]["points"]]
    #     if sum(points_dict[payer]) < 0:
    #         points_dict[payer] = 0
    # return points_dict


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    # app.run(debug=True)
    app.run(debug=True)

  

