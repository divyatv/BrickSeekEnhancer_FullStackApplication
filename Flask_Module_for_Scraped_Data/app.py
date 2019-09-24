from flask import Flask, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
import os

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
import connectDB
import pandas as pd

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

#################################################
# Database Setup
#################################################
# sql='SELECT * FROM market_scraped_data'
# entire_table=connectDB.connect_db(sql)

# df = pd.DataFrame(entire_table, columns =['priceoff', 'quantity', 'sku', 'storeaddress', 'zipcode']) 
# data_dict = df.T.to_dict().values()


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
    sql='SELECT * FROM market_scraped_data'
    entire_table=connectDB.connect_db(sql)

    df = pd.DataFrame(entire_table, columns =['priceoff', 'quantity', 'sku', 'storeaddress', 'zipcode']) 
    #df = df.reset_index(drop=True, inplace=True)
    data_dict = df.T.to_dict().values()
    js_var=str(data_dict).replace("(", "=")
    js_var_fixed=js_var.replace(")", ";")

    with open('static/dict_values.js', 'w') as file:
        file.write(js_var_fixed)
    # Return a list of df
    #return jsonify(data_dict) 
    return render_template("table_display.html")

@app.route("/plots")
def plots():
    """Return entire database entries fot a particular SKU""" 
    sql='SELECT * FROM market_scraped_data'
    entire_table=connectDB.connect_db(sql)

    df = pd.DataFrame(entire_table, columns =['priceoff', 'quantity', 'sku', 'storeaddress', 'zipcode']) 
    #df =df.reset_index(drop=True, inplace=True)
    data_dict = df.T.to_dict().values()

   
    return jsonify(data_dict)

    # Return a list of df
    #return jsonify(data_dict) 
    return jsonify(list(data_dict))   

if __name__ == "__main__":
    app.run()