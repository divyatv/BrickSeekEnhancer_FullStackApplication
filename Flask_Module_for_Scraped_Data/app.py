from flask import Flask, jsonify, render_template, json
import scrapebrickseekfinal
# from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly.graph_objs as go

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
import os
import sys

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect, Column, Integer, String, Float
import connectDB

from flask import request, redirect, Response, url_for, make_response
import random

import io
import uuid
import numpy as np

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

###############################################################
# Flask server for data extraction and rendering html
###############################################################
# 

#### Main route ############################################################################################
@app.route("/")
def home():
    """Return the homepage with a plot for team"""
    return render_template("homepage.html")
   
##### Get status of the stock #############################################################################
@app.route("/count/<user_sku>")
def count_result(user_sku):
   import sys
   print(user_sku,file=sys.stderr)
   mysqlQuery="SELECT quantity, COUNT(*) FROM market_scraped_data where sku=' "+str(user_sku)+" ' GROUP BY quantity"
   data = connectDB.connect_db(mysqlQuery)
   myresult = []
   for result in data:
       myresult.append({
           "Stock Status": result[0],
           "Stock Count": result[1]
       })
   return jsonify(myresult)

#### Get the table view for user filtering ###############################################################
@app.route("/table")
def table():
    """Return entire database entries for scraped data to be rendered in a table and filter""" 
    sql='SELECT * FROM walmart_scraped_data'
    entire_table=connectDB.connect_db(sql)

    df = pd.DataFrame(entire_table, columns =['priceoff', 'quantity', 'sku', 'storeaddress', 'zipcode']) 

    data_dict = df.T.to_dict().values()
    js_var=str(data_dict).replace("(", "=")
    js_var_fixed=js_var.replace(")", ";")

    with open('static/dict_values.js', 'w') as file:
        file.write(js_var_fixed)

    return render_template("table_display.html")

##############################################################################################################

@app.route('/scrape', methods=['GET','POST'])
def scrapedmap():
    return render_template("maps_display.html", jsonvalue= json.dumps(scrapebrickseekfinal.scrape_all()))

##############################################################################################################
@app.route("/stockstatus/<user_sku>/<user_upc>")
def stockstatus(user_sku, user_upc):
    """Return the page with plot of availability for the sku selected"""

    #sku = (' sku ',)
    #user_sku='201326711'
    import sys
    print(user_sku,file=sys.stderr)

    
    mysqlQuery="SELECT quantity, COUNT(*) FROM walmart_scraped_data where SKU='"+str(user_sku)+"' GROUP BY quantity"
    entire_table = connectDB.connect_db(mysqlQuery)

    # connection = engine.raw_connection()
    # cursor = connection.cursor()
    # #sql="SELECT zipcode, discount, COUNT(*) FROM market_scraped_data where sku=' "+str(user_sku)+" ' GROUP BY discount"
    # #entire_table=engine.execute("SELECT quantity, COUNT(*) FROM market_scraped_data WHERE sku= ' 201326711 ' GROUP BY quantity")
    # entire_table=engine.execute("SELECT quantity, COUNT(*) FROM market_scraped_data where sku=' "+str(user_sku)+" ' GROUP BY quantity")
    # cursor.close()

    df = pd.DataFrame(entire_table, columns =['quantity', 'count']) 
    # data_list = df.values.tolist()

    data = [
        go.Bar(
            x=df['quantity'], # assign x as the dataframe column 'x'
            y=df['count']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    import sys
    print(user_upc,file=sys.stderr)

    mysqlQuery="SELECT quantity, COUNT(*) FROM target_scraped_data where upc='"+str(user_upc)+"' GROUP BY quantity"
    entire_table = connectDB.connect_target_db(mysqlQuery)

    # connection = engine.raw_connection()
    # cursor = connection.cursor()
    # #sql="SELECT zipcode, discount, COUNT(*) FROM market_scraped_data where sku=' "+str(user_sku)+" ' GROUP BY discount"
    # #entire_table=engine.execute("SELECT quantity, COUNT(*) FROM market_scraped_data WHERE sku= ' 201326711 ' GROUP BY quantity")
    # entire_table=engine.execute("SELECT quantity, COUNT(*) FROM market_scraped_data where sku=' "+str(user_sku)+" ' GROUP BY quantity")
    # cursor.close()

    df1 = pd.DataFrame(entire_table, columns =['quantity', 'count']) 
    # data_list = df.values.tolist()

    data1 = [
        go.Bar(
            x=df1['quantity'], # assign x as the dataframe column 'x'
            y=df1['count']
        )
    ]
       
    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("lineplot.html", plot_war=graphJSON, plot_tar=graphJSON1)



############################################################################################################
@app.route("/plouuts/<sku>")
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
############################################################################################## 

### Running main function
if __name__ == "__main__":
    app.run(debug=True)