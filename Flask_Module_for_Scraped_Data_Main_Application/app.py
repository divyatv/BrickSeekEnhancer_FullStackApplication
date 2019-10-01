from flask import Flask, jsonify, render_template, json
import scrapebrickseekfinal

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

############Plot the map view#############################################################################################

@app.route('/scrape', methods=['GET','POST'])
def scrapedmap():
    return render_template("maps_display.html", jsonvalue= json.dumps(scrapebrickseekfinal.scrape_all()))

##############################################################################################################
@app.route("/stockstatus")
def stockstatus():
    """Return the page with plot of availability for the sku selected"""
    
    mysqlQuery_walmart="SELECT quantity, COUNT(*) FROM walmart_scraped_data where SKU='329264833' GROUP BY quantity"
    entire_tablew = connectDB.connect_db(mysqlQuery_walmart)

    dfw = pd.DataFrame(entire_tablew, columns =['quantity', 'count']) 
    # data_list = df.values.tolist()

    dataw = [
        go.Bar(
            x=dfw['quantity'], # assign x as the dataframe column 'x'
            y=dfw['count'],
            name="Walmart"
        )
    ]

    graphJSONW = json.dumps(dataw, cls=plotly.utils.PlotlyJSONEncoder)

    # import sys
    # print(user_upc,file=sys.stderr)

    mysqlQuery_target="SELECT quantity, COUNT(*) FROM target_scraped_data where upc='190198429612' GROUP BY quantity"
    entire_tablet = connectDB.connect_target_db(mysqlQuery_target)

    dft = pd.DataFrame(entire_tablet, columns =['quantity', 'count']) 
    # data_list = df.values.tolist()

    datat = [
        go.Bar(
            x=dft['quantity'], # assign x as the dataframe column 'x'
            y=dft['count'],
            name="Target"
            )
    ]
       
    graphJSONT = json.dumps(datat, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("barplot.html", plot_war=graphJSONW, plot_tar=graphJSONT)


############################################################################################################
### Running main function
if __name__ == "__main__":
    app.run(debug=True)
####################################################################################################
