from django.test import TestCase
from unittest.mock import MagicMock
from scraper_service import RunScraper
from scraper_service import NotificationSender
from products.models import Product, UserProduct, User
from datetime import datetime, timedelta
from django.utils import timezone
import math

class ScraperServiceRSMainTestCases(TestCase):
    product_2 = ('2', 'Best Buy', True, 42.00, 'B012', 'nya2.net', 'Two', '1_min')
    product_3 = ('3', 'Amazon', True, 0.01, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', 'nya3.org', 'Three', '10_min')
    product_4 = ('4', 'Custom Site', False, 0, '', 'nya4.org', 'Four', '1_hour')

    @classmethod
    def setUpClass(cls):
        super(ScraperServiceRSMainTestCases, cls).setUpClass()
        cls.run_scraper = RunScraper()
        cls.notification_sender = NotificationSender()

    def create_user_products(self, product_data, user_data, prod_per_user):
        # Format users as: (Username, password, email, discord webhook, phone number)
        # Format products as: (Name, supplier, stock, price, ID, url, nickname, refresh rate)

        # Creating an array for easy access of users in order of creation
        users = []
        # User creation
        for each in user_data:
            User.objects.create(username=each[0], password=each[1], email=each[2], discord_webhook_url=each[3], phone=each[4])
            users.append(User.objects.get(username=each[0]))

        # Ensuring that products per user is reasonable, otherwise making it spread across users evenly-ish
        num_users = len(user_data)
        num_products = len(product_data)
        if prod_per_user * num_users < num_products and num_users != 0:
            prod_per_user = math.ceil(num_products / num_users)

        # Create products associated with users in order provided,
        # associating prod_per_user products with each user in the order provided,
        # and having all "updated" 3 hours previously to ensure they update
        curr_user_num = 0
        num_products_with_user = 0
        for each in product_data:
            Product.objects.create(supplier=each[1], current_stock=each[2], current_price=each[3], product_id=each[4],
                                   last_updated=datetime.now(tz=timezone.utc) - timedelta(hours=3), product_name=each[0],
                                   product_url=each[5])
            UserProduct.objects.create(product=Product.objects.get(product_name=each[0]),
                                       product_nickname=each[6],
                                       username=users[curr_user_num], notification_interval=each[7])
            num_products_with_user = (num_products_with_user + 1) % prod_per_user
            if num_products_with_user == 0:
                curr_user_num += 1

    def fake_update_products(*args):
        for each in UserProduct.objects.all():
            each.product.last_updated = datetime.now(tz=timezone.utc)
            each.product.save()

    def test_main_small_mixed(self):
        """Running main on a set of UserProducts with one from each supplier should work as anticipated."""
        # Mocking update_products
        self.run_scraper.update_products = MagicMock(side_effect=self.fake_update_products)

        # Setting up database
        product_data = [self.product_2, self.product_3, self.product_4]
        user_data = [('User', 'thIsIsAP@ssword', 'nya@nya.org', '', '')]
        self.create_user_products(product_data, user_data, 3)

        # Running product update
        RunScraper.main(self.run_scraper)

        # Grabbing full object and testing for changes
        best_buy_object = Product.objects.get(product_name='2')
        amazon_object = Product.objects.get(product_name='3')
        custom_object = Product.objects.get(product_name='4')

        # Check that update_products ran properly, which updates timestamps
        # in UserProducts (should have updated within a minute)
        acceptable_time = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        self.assertGreater(best_buy_object.last_updated, acceptable_time,
                            "Updating Best Buy product should change the timestamp")
        self.assertGreater(best_buy_object.last_updated, acceptable_time,
                            "Updating Amazon product should change the timestamp")
        self.assertGreater(best_buy_object.last_updated, acceptable_time,
                            "Updating custom product should change the timestamp")

    # def test_main_large_mixed(self):
    #     """Running main on a set of UserProducts with one from each supplier should work as anticipated."""
    #     # Mocking update_products
    #     self.run_scraper.update_products = MagicMock(side_effect=self.fake_update_products)
    #
    #     # Setting up database
    #     product_data = [self.product_2, self.product_3, self.product_4]
    #     user_data = [('User', 'thIsIsAP@ssword', 'nya@nya.org', '', '')]
    #     self.create_user_products(product_data, user_data, 3)
    #
    #     # Storing old version of product object's timestamp data
    #     original_timestamp_BB = Product.objects.get(product_name='2').last_updated
    #     original_timestamp_amazon = Product.objects.get(product_name='3').last_updated
    #     original_timestamp_custom = Product.objects.get(product_name='4').last_updated
    #
    #     # Running product update
    #     RunScraper.main(self.run_scraper)
    #
    #     # Grabbing full object and testing for changes
    #     best_buy_object = Product.objects.get(product_name='2')
    #     amazon_object = Product.objects.get(product_name='3')
    #     custom_object = Product.objects.get(product_name='4')
    #
    #     # Check that update_products ran properly, which updates timestamps in UserProducts
    #     self.assertNotEqual(best_buy_object.last_updated, original_timestamp_BB,
    #                         "Updating Best Buy product should change the timestamp")
    #     self.assertNotEqual(amazon_object.last_updated, original_timestamp_amazon,
    #                         "Updating Amazon product should change the timestamp")
    #     self.assertNotEqual(custom_object.last_updated, original_timestamp_custom,
    #                         "Updating custom product should change the timestamp")