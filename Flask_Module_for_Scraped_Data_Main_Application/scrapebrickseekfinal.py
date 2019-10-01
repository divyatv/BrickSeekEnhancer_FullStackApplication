import requests
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
import re

# instantiate the splinter object 
def scrape_all():
    ## Connect to database and get the list of zip codes

    # DATABASE_URL = "postgres://bedlgjelgbrcba:62edbf5e39edf1ea129a38a5766d7354579374a6db487103a421c76fd47d78c3@ec2-184-73-232-93.compute-1.amazonaws.com:5432/dd4i4baf4sjibo"

    # engine = create_engine(DATABASE_URL)

    # ##zip_codes = [re.sub("\'|\,|\(|\)", "", str(item)) for item in engine.execute('SELECT zip FROM city_zip_data LIMIT 1').fetchall()]
    # zip_codes = ['27560']
    # for zip_code in zip_codes:
    #     url = 'https://brickseek.com/walmart-inventory-checker/'
    #     payload = {'search_method': 'sku', 'sku': '529623056', 'zip': zip_code, 'sort': 'price'}

    #     response = requests.post(url, data=payload)    # Make a POST request with data

    #     soup = BeautifulSoup(response.text, 'html.parser')

    #     results = soup.find('div', class_="table__body").find_all('div', class_="table__row")
    #     seeked_items = []
    #     for result in results:
    #         try:
    #             searched_zip = zip_code
    #             quantity = result.find('span', class_="table__cell-quantity")
    #             if not (quantity):
    #                 quantity = 0
    #             else:
    #                 quantity = int(re.search(r'\d+', quantity.text).group())
    #             availability = result.find('span', class_="availability-status-indicator__text").text
    #             store = re.sub(r"^\s+|\s+$", "",result.find('strong', class_="address-location-name").text)
    #             google_link = result.find_all('a', class_="address__link")[0]['href']
    #             gmaps_query = google_link.split("=",1)[1]
    #             store_zip = gmaps_query[-5:]
    #             price = ''.join(result.find('span', class_="price-formatted price-formatted--style-display").text)
    #             discount = result.find('span', class_="table__cell-price-discount")
    #             if not (discount):
    #                 discount = 'No Discount'
    #             else:
    #                 discount = discount.text
    #             # Get the Latitude and Longitude from Google api
    #             gkey = "AIzaSyDeMcxfAnuJB0TRF02BFDHVL_Wa5mfGMpc"
    #                 # Build the endpoint URL
    #             target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
    #                 'address={0}&key={1}').format(gmaps_query, gkey)
    #                 # Run a request to endpoint and convert result to json
    #             geo_data = requests.get(target_url).json()
    #             latitude = geo_data["results"][0]["geometry"]["location"]["lat"]
    #             longitude = geo_data["results"][0]["geometry"]["location"]["lng"]
    #             # Dictionary to be inserted as a List
    #             seeked = {
    #                 'Searched_Zip': searched_zip,
    #                 'Store_Name': store,
    #                 'Item_Price': price,
    #                 'Item_Quantity': quantity,
    #                 'Item_Availability': availability,
    #                 'Item_Discount': discount,
    #                 'Store_Zip': store_zip,
    #                 'Google_Maps': google_link,
    #                 'Google_Api_Query': gmaps_query,
    #                 'Store_Latitude': latitude,
    #                 'Store_Longitude': longitude
    #             }

    #             seeked_items.append(seeked)
    #         except AttributeError as e:
    #             seeked_items.append(e)
    # seeked_df = pd.DataFrame(seeked_items)
    # seeked_df.to_csv('seekeddataframe.csv',index=False)
    seeked_df = pd.read_csv("target_output.csv")
    return seeked_df.to_dict('records')