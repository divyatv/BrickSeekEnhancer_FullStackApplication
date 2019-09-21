import sqlalchemy
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
import connectDB

# Get zip codes from the city_zip_table
sql='SELECT zip FROM city_zip_data LIMIT 10'
zip=connectDB.connect_db(sql)

# Loop through all the zip codes and then build the url
import re
for item in zip:
 print (re.sub("\'|\,|\(|\)", "", str(item)))