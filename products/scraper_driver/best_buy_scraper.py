from selenium import webdriver
import os

class BestBuyScraper():
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
    # @return: Returns a float of the price of the item and if out of stock 0
    # @return: Returns True if the item is in stock otherwise false
    def get_price_bestbuy(self,url='https://www.bestbuy.com/site/combo/all-headphones/7cf1537f-9370-4db1-9b5c-b673c5c87e38'):
        
        if os.name == 'nt':
            driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self.options)
        else:
            driver = webdriver.Chrome(executable_path="/home/derek/StockCheck/chromedriver", options=self.options)

        driver.get(url)
        driver.implicitly_wait(self.implicit_wait_interval)
        #driver.get_screenshot_as_file('screenshot.png')


        price_element = driver.find_element_by_class_name('priceView-customer-price')
        price = price_element.find_element_by_tag_name('span').text

        try:
            temp_price = price.replace('$','')
            float_price = float(temp_price)
            return float_price, True
        except Exception as e:
            #print('Failed to get price data')
            pass
            

        add_cart_element = driver.find_element_by_class_name('add-to-cart-button')
        if add_cart_element.text == "Sold Out":
            return 0, False
        


    # @param product_sku: SKU for the product you're looking for 
    # @return: Returns a string with the link that can be used to find the price of the item
    def get_product_url_bestbuy(self,product_sku='5706659'):
        url = f'https://www.bestbuy.com/site/searchpage.jsp?st={product_sku}&_dyncharset=UTF-8'
        
        if os.name == 'nt':
            driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self.options)
        else:
            driver = webdriver.Chrome(executable_path="/home/derek/StockCheck/chromedriver", options=self.options)

        driver.get(url)
        driver.implicitly_wait(self.implicit_wait_interval)
        #driver.get_screenshot_as_file('screenshot.png')

        if 'search' not in driver.current_url:
            #print("Already got the url")
            return driver.current_url

        header_element = driver.find_element_by_class_name('sku-header')
        link_element = header_element.find_element_by_tag_name('a')
        link = link_element.get_attribute('href')

        return link

