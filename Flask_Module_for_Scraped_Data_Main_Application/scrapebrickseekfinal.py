# Import the dependencies and modules required
import requests
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
import re
from config import gkey

# Scrape data from the brickseek portal/from the combined html file with data
def scrape_fromhtml():
    # Use beautiful soup in order to scrape the data from the combined html file
    html_file = 'Resources/combined_walmart.html'

    soup = BeautifulSoup(open(html_file), 'html.parser')
    
    results = soup.find_all('div', class_="table__body")
    # Declare empty list to get the list of dictionaries
    seeked_items = []
    for result in results:
        # Get the rows with the data based on the class name
        rows = result.find_all('div', class_="table__row")
        for row in rows:
            # Exception Handeling
            try:
                # Scrape the items required for the map view
                quantity = row.find('span', class_="table__cell-quantity")
                if not (quantity):
                    quantity = 0
                else:
                    quantity = int(re.search(r'\d+', quantity.text).group())

                availability = row.find('span', class_="availability-status-indicator__text").text
                store = re.sub(r"^\s+|\s+$", "",row.find('strong', class_="address-location-name").text)
                google_link = row.find_all('a', class_="address__link")[0]['href']
                gmaps_query = google_link.split("=",1)[1]
                store_zip = gmaps_query[-5:]
                price = ''.join(row.find('span', class_="price-formatted price-formatted--style-display").text)
                discount = row.find('span', class_="table__cell-price-discount")

                if not (discount):
                    discount = 'No Discount'
                else:
                    discount = discount.text

                # Get the Latitude and Longitude from Google api
                # gkey = ""
                # Build the endpoint URL
                target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
                    'address={0}&key={1}').format(gmaps_query, gkey)
                # Run a request to endpoint and convert result to json
                geo_data = requests.get(target_url).json()
                # Exception handeling for index error in case the data is not found
                try:
                    latitude = geo_data["results"][0]["geometry"]["location"]["lat"]
                    longitude = geo_data["results"][0]["geometry"]["location"]["lng"]
                except IndexError:
                    continue
                # Dictionary to be inserted as a List
                seeked = {
                    'Store_Name': store,
                    'Item_Price': price,
                    'Item_Quantity': quantity,
                    'Item_Availability': availability,
                    'Item_Discount': discount,
                    'Store_Zip': store_zip,
                    'Google_Maps': google_link,
                    'Google_Api_Query': gmaps_query,
                    'Store_Latitude': latitude,
                    'Store_Longitude': longitude
                }

                seeked_items.append(seeked)
            except AttributeError as e:
                seeked_items.append(e)
    # Convert list into Dataframe
    seeked_df = pd.DataFrame(seeked_items)
    seeked_df = seeked_df.drop_duplicates()
    seeked_df.to_csv("Resources/walmart_output.csv",index=False)
    return seeked_df

def scrape_all():

    # Get the records from the scrape function for it to be called by the flask code

    ######### Uncomment the below two lines of code for validation (Runs for 8 Minutes)######## Last two lines for demo alone#######
    # import_dataframe = scrape_fromhtml()

    # return import_dataframe.to_dict('records')

    ########## Code for demo just to read the file from the scraped CSV #############

    scrapedcsv_df = pd.read_csv("Resources/walmart_output.csv")

    return scrapedcsv_df.to_dict('records')

### Instantiating Empty Constructer
if __name__ == "__main__":
    pass
