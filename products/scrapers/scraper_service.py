from products.models import Product, UserProduct
from products.scrapers.best_buy_scraper import BestBuyScraper
import django
import datetime, os
from products.scrapers.amazon_scraper import amazon_scraper
os.chdir('../../core/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StockCheck.settings")
django.setup()
from core.models import *
import pytz
from collections import defaultdict
import time
from notifications.notifications import sendEmail
import threading

class RunScraper():
    def create_product_dict(self):
        all_products = Product.objects.all()
        for product in all_products:
            self.product_dict[product.product_name] = product.last_updated

    def update_prodcuts(self,products):
        for product in products:
            if product.supplier == 'bestbuy':
                print('Trying to get bestbuy')
                b = BestBuyScraper()
                url = b.get_product_url_bestbuy(product.product_id)
                price, stock = b.get_price_bestbuy(url)
                #print(f'Price is {price} stock is {stock}')
                product.current_price = price
                product.current_stock = stock
                product.last_updated = pytz.utc.localize(datetime.datetime.utcnow())
                product.save()
            elif product.supplier == 'Amazon':
                print('Trying to get amazon ')
                stock, price, name = amazon_scraper(product.product_url)
                product.current_stock = stock
                product.current_price = price
                product.name = name
                product.last_updated = pytz.utc.localize(datetime.datetime.utcnow())
                product.save()

    def main(self):
        
        user_products = UserProduct.objects.all()
        
        # key is product object val is whether or not the product has been updated
        products_dict = defaultdict(lambda:0)   
        products_to_update = []

        for each in user_products:
            #print(each.product_object)
            product = each.product_object
            notification_interval = each.notification_interval
            num, unit = notification_interval.split('_')

            if unit == 'hour':
                now = pytz.utc.localize(datetime.datetime.utcnow())
                if product.last_updated < now - datetime.timedelta(hours=int(num)):
                    print('Need to update')
                    notification = NotificationQueue(username=each.username,notification_method=each.notification_method)
                    notification.save()
                    if products_dict[product] == 0:
                        products_to_update.append(product)
                        products_dict[product] = 1

            elif unit == 'min':
                now = pytz.utc.localize(datetime.datetime.utcnow())
                if product.last_updated < now - datetime.timedelta(minutes=int(num)):
                    print('Need to update')
                    notification = NotificationQueue(username=each.username,notification_method=each.notification_method)
                    notification.save()
                    if products_dict[product] == 0:
                        products_to_update.append(product)
                        products_dict[product] = 1

        self.update_prodcuts(products_to_update)
        

class NotificationSender():

    def send_notifcations(self):
        notifications = NotificationQueue.objects.all()
        for each in notifications:
            if each.notification_method == 'Email':
                send_to = each.username.email
                message = f"You have an update for a product"
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

if __name__ == '__main__':
    main()


