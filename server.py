"""Server for Fetch Rewards application"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

import os
import requests
from jinja2 import StrictUndefined
from datetime import date, timedelta, datetime


app = Flask(__name__)

app.secret_key = "dev" 
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["API_KEY"]

@app.route('/')
def homepage():
    #should this page have a form to collect transaction inputs?
    #and a button for each route?
    return render_template("homepage.html")


@app.route('/transaction')
def add_transaction(payer, points, timestamp):
    """Add transactions for a specific payer and date."""
    

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

@app.route('/balances')
def all_balances():
    """Return all payer point balances.
    {
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 5300
    }"""