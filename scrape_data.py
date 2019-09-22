#from __future__ import division, unicode_literalsi
### This file has functions which will scrape data from brick seek
### Then load the data that was craped into postgres database.
#### Postgres database is running on heroku
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


def scrape_endpoint(sku):
    # Get zip codes from the city_zip_table
    ## select zip from city_zip_data where it matches the SKU provided- change later
    sql='SELECT zip FROM city_zip_data LIMIT 10'
    zip_code=connectDB.connect_db(sql)

    # Loop through all the zip codes and then build the url 
    zip_codes=[]
    for item in zip_code:
        zip_codes.append(re.sub("\'|\,|\(|\)", "", str(item)))
    ##return(zip_codes)
    ### Make http calls using curl command and fetch the data required.
    for item in zip_codes:
        command= 'curl --data ' + '"sku=' + str(sku) + '&zip=' + item + \
                  '" https://brickseek.com/walmart-inventory-checker? -o html'+ item +'.html'
        os.system(command) 
    return(zip_codes)    
    

def read_from_html(htmlfile_name):        
    filepath = os.path.join(htmlfile_name)
    with open(filepath, encoding='utf-8') as file:
        read_html_content = file.read()
        return (read_html_content)

def scrape_html_pages(zip_code):
    try:         
    
        soup = BeautifulSoup(read_from_html('html'+ zip_code +'.html'), 'html.parser')
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
        pages_dict = [ {"sku": sku, "zip-code:":  address_ex[i].split()[-1], "price-off": discount[i], \
                        "store-address" : ' '.join(address_ex[i].split()[:-1]), \
                        "quantity": quantity[i] } for i in range(len(discount)) ]
        #for page in pages_dict:
        #    print(page) 
        return pages_dict 

    except AttributeError: 
        print("Sorry ! You are dividing by zero ")    
    except FileNotFoundError: 
        print("File not found move on ")     

def write_to_db(zip_codes):

    page_dict_list = []
    # for item in  [scrape_html_pages(item) for  item in zip_codes]:
    #     page_dict_list = page_dict_list + item

    for every in zip_codes:
        page_dict_list.append(scrape_html_pages(every))
    
    for i in page_dict_list:
        print("iiiii",  i)

    # drop city_zip_data if it exist already
    rds_connection_string = "bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    engine.table_names()
    market_scraped_data = 'market_scraped_data'
    connection = engine.raw_connection()
    cursor = connection.cursor()
    command = "DROP TABLE IF EXISTS {};".format(market_scraped_data)
    cursor.execute(command)
    connection.commit()
    cursor.close()
       
    pages_data_df = pd.DataFrame.from_dict(page_dict_list)
    pages_data_df=pages_data_df.dropna()
    pages_data_df.head(10)
    #df1.to_sql('users', con=engine, if_exists='append')
    pages_data_df.to_sql('market_scraped_data', con=engine, index=False, if_exists='append',dtype={col_name: sqlalchemy.types.VARCHAR for col_name in pages_data_df})
    #pd.read_sql_query('select * from market_scraped_data', con=engine).head()
    # print(page_dict_list)    


if __name__ == '__main__' :
    sku = 940939534
    
    zip_codes=scrape_endpoint(sku)
    #print(zip_codes)
    
    write_to_db(zip_codes)
    # for item in zip_codes:
    #     s.remove('html'+ item +'.html')

##### Remove the html files that were generated.
    for item in zip_codes:
        file = 'html' + item + '.html'
        if os.path.exists(file):
            os.remove(file)

           

     
    
