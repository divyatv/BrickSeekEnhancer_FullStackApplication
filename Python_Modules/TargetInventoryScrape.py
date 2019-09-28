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
    sql='SELECT zip FROM city_zip_data'
    zip_code=connectDB.connect_db(sql)

    # Loop through all the zip codes and then build the url 
    zip_codes=[]
    for item in zip_code:
        zip_codes.append(re.sub("\'|\,|\(|\)", "", str(item)))
    ##return(zip_codes)
    ### Make http calls using curl command and fetch the data required.
    for item in zip_codes:
        command= 'curl --data ' + '"sku=' + str(sku) + '&zip=' + item + \
                  '" https://brickseek.com/target-inventory-checker? -o html'+ item +'.html'
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
        pages_dict = [ {"sku": sku, "zipcode:":  address_ex[i].split()[-1], "priceoff": discount[i], \
                        "storeaddress" : ' '.join(address_ex[i].split()[:-1]), \
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
    rds_connection_string = "postgres://wyscmkyadpxnpq:4035077d37da67ed9b5c3f7d5a1560ed3adfda8c7e7a875df5139b38e8e5561e@ec2-54-83-201-84.compute-1.amazonaws.com:5432/d77gdrm2h45ur9"
    engine = create_engine(f'postgresql://{rds_connection_string}')
    # engine.table_names()
    # market_scraped_data = 'market_scraped_data'
    # connection = engine.raw_connection()
    # cursor = connection.cursor()
    # command = "DROP TABLE IF EXISTS {};".format(market_scraped_data)
    # cursor.execute(command)
    # connection.commit()
    # cursor.close()
       
    pages_data_df = pd.DataFrame.from_dict(page_dict_list)
    pages_data_df=pages_data_df.dropna()
    pages_data_df.head(10)
    #df1.to_sql('users', con=engine, if_exists='append')
    pages_data_df.to_sql('target_scraped_data', con=engine, index=False, if_exists='append',dtype={col_name: sqlalchemy.types.VARCHAR for col_name in pages_data_df})
    #pd.read_sql_query('select * from market_scraped_data', con=engine).head()
    # print(page_dict_list)    


if __name__ == '__main__' :
    sku = '080-02-1714'
    
    zip_codes=scrape_endpoint(sku)
    #print(zip_codes)
    
    write_to_db(zip_codes)
    # for item in zip_codes:
    #     s.remove('html'+ item +'.html')

##### Remove the html files that were generated.
    # for item in zip_codes:
    #     file = 'html' + item + '.html'
    #     if os.path.exists(file):
    #         os.remove(file)

           

     
    
