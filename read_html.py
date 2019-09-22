import sqlalchemy
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
import connectDB
import re
import os 
import codecs
import pandas as pd

def connect_db(sql):

            rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
            engine = create_engine(f'postgresql://{rds_connection_string}')
            return engine.execute(sql).fetchall()

def read_from_html(htmlfile_name):        
    #filepath = os.path.join(htmlfile_name)
    with open(htmlfile_name, encoding='utf-8') as file:
        read_html_content = file.read()
        return (read_html_content)

import sys
import glob
import errno


def calculate_dict(path):
    #path = path   
    files = glob.glob(path)
    for file in files:
        with open(file, encoding='utf-8') as file:
          read_html_content = file.read()
        soup = BeautifulSoup(read_html_content, 'html.parser')
        all_data = soup.find('div', class_="table inventory-checker-table inventory-checker-table--store-availability-price inventory-checker-table--columns-3")
            # .find('span', class_="table__cell-price-discount")
        price_value=all_data.find_all('span', class_='table__cell-price-discount')
            #print(price_value)  
        discount=[ item.text for item in price_value ]
            #print("divya", discount)
        address_ex = [item.text.split('\n')[1] for item in all_data.find_all('address', class_='address') ]
            #print("address", address_ex)
        quantity=[ indi.text for indi in all_data.find_all('span', class_='availability-status-indicator__text') ]
            #print("quantity", quantity)
        s=soup.find_all('div', class_='item-overview__meta-item')[1].text
        import re
        sku_search = re.search('\nSKU:(.*)', s)
        sku=sku_search.group(1)

        pages_dict = [ {"sku": sku, "zip-code:":  address_ex[i].split()[-1], "price-off": discount[i], \
                            "store-address" : ' '.join(address_ex[i].split()[:-1]), \
                            "quantity": quantity[i] } for i in range(len(discount)) ]
            #for page in pages_dict:
            #    print(page) 
        return pages_dict

page_dict_list = []
    # for item in  [scrape_html_pages(item) for  item in zip_codes]:
    #     page_dict_list = page_dict_list + item
    
sql='SELECT zip FROM city_zip_data LIMIT 10'
zip_code=connect_db(sql)
zip_codes=[]

for item in zip_code:
    zip_codes.append(re.sub("\'|\,|\(|\)", "", str(item)))

for every in zip_codes:
    page_dict_list.append(calculate_dict('../html_files_night/*.html'))

rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
engine = create_engine(f'postgresql://{rds_connection_string}') 
   
for i in page_dict_list:
    print("iiiii",  i)

   
    pages_data_df = pd.DataFrame.from_dict(i)
#pages_data_df=pages_data_df.dropna()
    pages_data_df.head(10)
    #df1.to_sql('users', con=engine, if_exists='append')
    pages_data_df.to_sql('market_scraped_data', con=engine, index=False, if_exists='append',dtype={col_name: sqlalchemy.types.VARCHAR for col_name in pages_data_df})
    #pd.read_sql_query('select * from market_scraped_data', con=engine).head()
    # print(page_dict_list)    

