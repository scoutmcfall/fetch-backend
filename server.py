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