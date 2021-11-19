from bs4 import BeautifulSoup
import requests


def amazon_scraper(url):
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

# stock, price, name = amazon_scraper('https://www.amazon.com/gp/product/B07YLRX7P2?pf_rd_r=YFJDSCD7X4QDAYYG0FEY&pf_rd_p=1ab92b69-98d7-4842-a89b-ad387c54783f&pd_rd_r=d001666d-3c8c-44fe-a2b0-88d474621439&pd_rd_w=PSrWO&pd_rd_wg=kwJwk&ref_=pd_gw_unk')
# print(f'Name: {name} price {price} stock {stock}')