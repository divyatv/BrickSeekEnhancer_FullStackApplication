import requests
from lxml import html

url = 'https://brickseek.com/walmart-inventory-checker/'
payload = {'search_method': 'sku', 'sku': '182740213', 'zip': '75082', 'sort': 'price'}

r = requests.post(url, data=payload)    # Make a POST request with data

tree = html.fromstring(r.content)    # Parse response from the page with lxml.html

stores = tree.xpath('//tr[.//h4]')    # Get all stores from the page

for store in stores:    # In the loop get and save in the dictionary all desired info
    item = dict()
    item['MSRP'] = ''.join(store.xpath('td/span[@class="price-formatted price-formatted"]/strong/text()'))
    item['Store-name'] = ''.join(store.xpath('td/h4/text()'))
    item['Store-address'] = ' '.join(store.xpath('td/address/text()'))
    item['Quantity'] = ''.join(store.xpath('td/span[@class="store-quan"]/strong/text()'))
    item['Price'] = ''.join(store.xpath('td[@class="store-price"]/span/text()')).strip()
    print(item)