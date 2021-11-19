from bs4 import BeautifulSoup
import requests


def custom_site_scraper(url, search_element):
    try:
        id_search = "availability"
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)}'
                                  'AppleWebKit/537.36 (KHTML, like Gecko))'
                                  'Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'})
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.content, features="html.parser")
        price = soup.find('span', {'class': 'a-price'}).get_text().strip()
        price = price[0:int(len(price) / 2)]
        data = soup.find(id=id_search)
        data = data.find('span', {'class': 'a-size-medium'}).text.strip()
        name = soup.find('span', {'id': 'productTitle'}).text.strip()
        price = price.replace('$','')
        price = float(price)
        if not data:
            data = 'Out of Stock'
            return False, price, name
        return True, price, name
    except AttributeError:
        data = 'Out of Stock.'
        price = 0
        return False, price, name