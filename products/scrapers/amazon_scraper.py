from bs4 import BeautifulSoup
import requests
from requests.exceptions import MissingSchema


def amazon_scraper(url):
    # id_search = "availability"
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)}'
                                'AppleWebKit/537.36 (KHTML, like Gecko))'
                                'Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
                
    # Ensure that some sort of scheme is provided
    if not (url.__contains__("https://") or url.__contains__("http://")):
        url = "https://" + url

    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.content, features="html.parser")
    buy_now_button = soup.select('#buy-now-button')
    add_cart_button = soup.select('#add-to-cart-button')
    
    try:
        name = soup.find('span', {'id': 'productTitle'}).text.strip()
    except AttributeError as e:
        raise MissingSchema
    if len(buy_now_button) == 0 and len(add_cart_button) == 0:
        print('No buy now button')
        stock = False
        price = 0
        return stock, price, name
    else:
        stock = True
    price_element = soup.select('#twister-plus-price-data-price')
    price = price_element[0]['value']
    unit_element = soup.select('#twister-plus-price-data-price-unit')
    unit = unit_element[0]['value']
    
    if unit != '$' and price[-1] == '0' and price [-2] == '0':
        price = price[:-2]
    
    price = price.replace('$', '')
    price = price.replace(',', '')
    price = float(price)
    #soup = BeautifulSoup(r.content, features="html.parser")
    #stock = soup.find('span', {'id': 'submit.buy-now'}).text.strip()
    if not stock:
        return False, price, name
    return True, price, name
    
    