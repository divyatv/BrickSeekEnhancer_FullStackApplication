from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    inv_deals = {}

    url = "https://brickseek.com/walmart-inventory-checker/?sku=759605592"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    inv_deals["SKU"] = soup.find("body", class_="result-title").get_text()
    <div class="item-overview__meta-item"><strong>SKU:</strong> 759605592 </div>

    inv_deals["MSRP"] = soup.find("span", class_="result-price").get_text()
    <span class="price-formatted price-formatted--style-normal">$9.84</span>

    inv_deals["Store"] = soup.find("span", class_="result-hood").get_text()
    <a href="/walmart-clearance-stores/?store=4484">Walmart Supercenter #4484</a>

    inv_deals["Address"] = soup.find("span", class_="result-hood").get_text()
    <address class="address ">
    8000 Town Dr.<br>Raleigh NC 27616 <div class="address__below">
    (6.2 Miles Away) </div>
    <div class="address__links">
    <a class="address__link" href="https://maps.google.com/maps?q=8000+Town+Dr.+Raleigh+NC+27616" target="_blank" rel="noopener noreferrer">Google Maps</a>
    <span class="address__link-separator"></span>
    <a class="address__link" href="http://maps.apple.com/?address=8000+Town+Dr.+Raleigh+NC+27616">Apple Maps</a>
    </div>
    </address>

    inv_deals["Availability"] = soup.find("span", class_="result-hood").get_text()
    <span class="availability-status-indicator__text">Limited Stock</span>

    inv_deals["Price"] = soup.find("span", class_="result-hood").get_text()
    <span class="price-formatted price-formatted--style-display"><span class="price-formatted__currency">$</span><span class="price-formatted__dollars">9</span><span class="price-formatted__decimal">.</span><span class="price-formatted__cents">84</span></span>

    return  inv_deals

    def Walmart(SKU, ZIP):
	data = {
		'SKU': SKU,
        'MSRP' : MSRP,
        'Store' : Store,
        'Address' : Address,
        'Availability' : Availability,
        'Price' : Price,
		'sort': 'distance'
		}