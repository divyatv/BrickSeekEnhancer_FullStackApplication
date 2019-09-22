import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
import connectDB
import pandas as pd
 

sql='SELECT * FROM market_scraped_data'
entire_table=connectDB.connect_db(sql)

df = pd.DataFrame(entire_table, columns =['index', 'price-off', 'quantity', 'sku', 'store-address', 'zip-code:']) 
data_dict = df.T.to_dict().values()

with  open('tabledata.js', 'w') as file:
    file.write(str(data_dict))
#print(data_dict)