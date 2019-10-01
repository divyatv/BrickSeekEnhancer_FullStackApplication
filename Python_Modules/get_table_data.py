import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
import connectDB
import pandas as pd
 

sql='SELECT * FROM market_scraped_data'
entire_table=connectDB.connect_db(sql)

df = pd.DataFrame(entire_table, columns =['priceoff', 'quantity', 'DCPI', 'storeaddress', 'zipcode']) 
data_dict = df.T.to_dict().values()

df.to_csv(r'database_dmp.csv')

# with  open('data.js', 'w') as file:
#     file.write(str(data_dict))
#print(data_dict)