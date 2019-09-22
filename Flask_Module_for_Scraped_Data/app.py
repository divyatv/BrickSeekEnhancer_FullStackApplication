from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    """Return the homepage."""
    return render_template("homepage.html")

@app.route("/maps")
def render_dict_maps():
    """Return the dictionary for harsha"""

@app.route("/table")
def table():
    """Return entire database entries fot a particular SKU"""  
    return render_template("table_display.html")

if __name__ == "__main__":
    app.run()