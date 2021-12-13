from bs4.element import ProcessingInstruction
import django
import datetime, os
from products.scrapers.amazon_scraper import amazon_scraper
# os.chdir('../../core/')
os.chdir('./core/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StockCheck.settings")
django.setup()
os.chdir('..')
from core.models import *
import pytz
from collections import defaultdict
import time
from notifications.notifications import sendEmail
import threading
from products.models import Product, UserProduct
from products.scrapers.best_buy_scraper import BestBuyScraper

class RunScraper():

    def update_products(self, products):
        for each in products:
            product = each.product
            if product.supplier == 'Best Buy':
                print('Trying to get bestbuy')
                b = BestBuyScraper()
                stock, price, name = b.get_price_bestbuy(product.product_url)
                if str(price) != str(product.current_price):
                    print('Going to email')
                    message = f'Price of {each.product_nickname} changed to {price}'
                    notification = NotificationQueue(username=each.username,notification_method=each.notification_method,message=message)
                    notification.save()
                #print(f'Price is {price} stock is {stock}')
                
                product.current_price = price
                product.current_stock = stock
                product.last_updated = pytz.utc.localize(datetime.datetime.utcnow())
                product.save()
            elif product.supplier == 'Amazon':
                try:
                    print('Trying to get amazon ')
                    stock, price, name = amazon_scraper(product.product_url)
                    if str(price) != str(product.current_price):
                        print('Going to email')
                        message = f'Price of {each.product_nickname} changed to {price}'
                        notification = NotificationQueue(username=each.username,notification_method=each.notification_method,message=message)
                        notification.save()
                    product.current_stock = stock
                    product.current_price = price
                    product.name = name
                    product.last_updated = pytz.utc.localize(datetime.datetime.utcnow())
                    product.save()
                    print(f'Results were {stock}:{price}:{name}')
                except Exception as e:
                    print('Ran into a problem with amazon')

    def main(self):
        
        user_products = UserProduct.objects.all()
        
        # key is product object val is whether or not the product has been updated
        products_dict = defaultdict(lambda:0)   
        products_to_update = []

        for each in user_products:
            #print(each.product_object)
            product = each.product
            notification_interval = each.notification_interval
            num, unit = notification_interval.split('_')

            if unit == 'hour':
                now = pytz.utc.localize(datetime.datetime.utcnow())
                if product.last_updated < now - datetime.timedelta(hours=int(num)):
                    
                    
                    if products_dict[product] == 0:
                        print('Need to update')
                        products_to_update.append(each)
                        products_dict[product] = 1

            elif unit == 'min':
                now = pytz.utc.localize(datetime.datetime.utcnow())
                if product.last_updated < now - datetime.timedelta(minutes=int(num)):
                    
                    # notification = NotificationQueue(username=each.username,notification_method=each.notification_method)
                    # notification.save()
                    if products_dict[product] == 0:
                        print('Need to update')
                        products_to_update.append(each)
                        products_dict[product] = 1

        self.update_products(products_to_update)
        

class NotificationSender():

    def send_notifcations(self):
        notifications = NotificationQueue.objects.all()
        for each in notifications:
            if each.notification_method == 'Email':
                send_to = each.username.email
                message = each.message
                #message = f"You have an update for a product"
                subject = "Stock change"
                sendEmail(send_to,'derekfran55@gmail.com',subject,message)
            if each.notification_method == 'SMS':
                pass
            
            each.delete()

def main():
    s = RunScraper()
    n = NotificationSender()
    while True:
        s.main()
        t = threading.Thread(target=n.send_notifcations)
        t.start()
        t.join()
        time.sleep(.5)

def notify():
    n = NotificationSender()
    while True:
        n.send_notifcations()
        time.sleep(.5)

if __name__ == '__main__':
    main()


