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
    res = requests.get(url)



@app.route('/transaction')
def add_transaction(payer, date):
    """Add transactions for a specific payer and date."""

@app.route('/spend')
def spend_points():
    """● Spend points using the rules above and return a list of 
    { "payer": <string>, "points": <integer> } for each call."""

@app.route('/balances')
def all_balances():
    """Return all payer point balances."""