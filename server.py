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
        if transaction["points"] > 0:
            ledger = session.get("ledger", [])
            ledger.append((timestamp, points, payer))
            session["ledger"] = ledger
        else:
            negs = session.get("negs", [])
            negs.append((timestamp, points, payer))
            session["negs"] = negs
            #now the list of negative transations can be processed in the spend route against the postive transactions in ledger
    print("************************************")

    print(session["ledger"])
    print("************************************")

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
    else:
        negs = session.get("negs", [])
        negs.append((timestamp, points, payer))
        
   
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
    
    negs = session["negs"]
    ledger = sorted(session["ledger"])
    spend = request.args
   
    cost = int(spend.get("points", 0))

    for timestamp, points, payer in negs:
        cost += int(points) 
    
    #sum up all points for all payers
    spending_limit = 0
    print("************************************")

    print(ledger)
    print("************************************")

    print(negs)
    print("************************************")

    for transaction in ledger:
        points = transaction[1]
        spending_limit += points
    
    #now my spending limit is the total of all pts in ledger
    #i need to iterate through the ledger, subtracting points from my spending limit until the sl is 0
    #and each time a transaction in ledger is zeroed out, erase it from the ledger
    
    #cost is what i'm supposed to spend total
    for transaction in ledger:
        if spending_limit == 0:
            break
        points = int(transaction[1])
        if cost >= points:
            ledger.remove(transaction)
            cost -= points
            spending_limit -= points
        else:
            #if what i'm subtracting is less than the oldest point amount, 
            # i update that oldest point amount and break out of the loop
            ledger.append((transaction[0], points-cost, transaction[2]))
            ledger.remove(transaction)
            break

    #zero out negs once i've subtracted them all
    session["negs"] = []
    print("************************************")
    print(session["ledger"])
    print("************************************")

    print(session["negs"])

    return("", 200)


@app.route('/balances',  methods=["GET"])
def all_balances():
    """Return all payer point balances. If negative, reset to 0.
    {
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
    }"""
    ledger = session["ledger"]
    balance = {}
    for transaction in ledger:
        payer = transaction[2]
        points = transaction[1]
        balance[payer] = balance.get(payer, points)
    print(balance)
    session["balance"] = balance
    return("", 200)



if __name__ == "__main__":
    
    app.run(debug=True)

  

