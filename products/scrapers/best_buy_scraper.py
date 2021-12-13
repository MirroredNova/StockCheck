from selenium import webdriver
import os

from StockCheck.settings import CHROMEDRIVER_PATH


class BestBuyScraper:
    def __init__(self) -> None:
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('log-level=3')

        self.implicit_wait_interval = 2

    # @param url: String with the url of the item that you're trying to find the price of
    # @return: Returns True if the item is in stock otherwise false
    # @return: Returns a float of the price of the item and if out of stock 0
    # @return: Returns a string of the product name, if found (currently just blank for testing)
    def get_price_bestbuy(self, url):
        # Ensure that some sort of scheme is provided
        if not (url.__contains__("https://") or url.__contains__("http://")):
            url = "https://" + url

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=self.options)

        driver.get(url)
        driver.implicitly_wait(self.implicit_wait_interval)
        # driver.get_screenshot_as_file('screenshot.png')

        price_element = driver.find_element_by_class_name('priceView-customer-price')
        price = price_element.find_element_by_tag_name('span').text
        name_element = driver.find_element_by_class_name('heading-5')
        name = name_element.text

        temp_price = price.replace('$', '')
        temp_price = temp_price.replace(',','')
        float_price = float(temp_price)


        add_cart_element = driver.find_element_by_class_name('add-to-cart-button')
        if add_cart_element.text == "Sold Out":
            return False, 0, name
        
        return True, float_price, name
