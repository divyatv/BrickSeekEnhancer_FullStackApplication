from flask import Flask, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly.graph_objs as go

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

from flask import json

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
    sql="SELECT quantity, COUNT(*) FROM market_scraped_data where sku=' 600104275 ' GROUP BY quantity"
    entire_table=connectDB.connect_db(sql)
    df = pd.DataFrame(entire_table, columns =['quantity', 'count']) 
    # data_list = df.values.tolist()

    data = [
        go.Bar(
            x=df['quantity'], # assign x as the dataframe column 'x'
            y=df['count']
        )
    ]
       
    # with open('static/data_list_values.js', 'w') as file:
    #     file.write(str(data_list))

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("homepage.html", plot=graphJSON)

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

@app.route("/plots/<sku>")
def plots(sku):
    """Return entire database entries fot a particular SKU""" 
    sku = (' sku ',)
  

    rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    #engine.table_names()
    connection = engine.raw_connection()
    cursor = connection.cursor()
    entire_table=engine.execute('SELECT priceoff, zipcode, quantity FROM market_scraped_data WHERE sku= %s', sku)
    cursor.close()

    df = pd.DataFrame(entire_table, columns =['priceoff', 'zipcode', 'quantity'])

    zipc = df['zipcode'].tolist()
    valuesc=df['priceoff'].tolist()
    labels=[]
    values=[]
    legend = 'Location'
    for item in zipc:
        labels.append(str(item))
    for item in valuesc:
        values.append(str(item).replace("% off", ""))
      
    return render_template('Chart.html', values=values, labels=labels, legend=legend)
    # Return a list of df
    #return jsonify(data_dict) 
    #return jsonify(list(data_dict))   

if __name__ == "__main__":
    app.run(debug=True)