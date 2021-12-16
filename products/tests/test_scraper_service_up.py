from django.test import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import scraper_service
from scraper_service import RunScraper
from scraper_service import NotificationSender
from scraper_service import main
from products.models import Product, UserProduct, User
from datetime import datetime
from django.utils import timezone

class ScraperServiceUPTestCases(TestCase):

    product_2 = ('2', 'Best Buy', True, 42.00, 'B012', 'nya2.net', 'Two')
    product_3 = ('3', 'Amazon', True, 0.01, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', 'nya3.org', 'Three')
    product_4 = ('4', 'Custom Site', False, 0, '', 'nya4.org', 'Four')

    @classmethod
    def setUpClass(cls):
        super(ScraperServiceUPTestCases, cls).setUpClass()
        cls.run_scraper = RunScraper()
        cls.notification_sender = NotificationSender()

    def create_user_products(self, product_data):
        # Populating database, starting with setting up product data and a user
        # Format inputs as: (Name, supplier, stock, price, ID, url, nickname)
        User.objects.create_user('User', 'a@b.com', '1254NYA')
        # Creating products and userproducts
        for each in product_data:
            Product.objects.create(supplier=each[1], current_stock=each[2], current_price=each[3], product_id=each[4],
                                   last_updated=datetime.now(tz=timezone.utc), product_name=each[0],
                                   product_url=each[5])
            UserProduct.objects.create(product=Product.objects.get(product_name=each[0]),
                                       product_nickname=each[6],
                                       username=User.objects.get(username='User'))

    @patch('scraper_service.custom_site_scraper')
    @patch('scraper_service.amazon_scraper')
    @patch('scraper_service.BestBuyScraper')
    def test_update_products_empty(self, mock_best_buy_scraper, mock_amazon_scraper, mock_custom_site_scraper):
        """Updating an empty list of products should not cause any uncaught errors"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_amazon_scraper.side_effect = [(True, 9.50, "1"), (True, 0.05, "3")]
        mock_custom_site_scraper.side_effect = [True]

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

    @patch('scraper_service.custom_site_scraper')
    @patch('scraper_service.amazon_scraper')
    @patch('scraper_service.BestBuyScraper')
    def test_update_products_one_best_buy(self, mock_best_buy_scraper, mock_amazon_scraper, mock_custom_site_scraper):
        """Updating a list with a single product from Best Buy should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]

        mock_amazon_scraper.side_effect = [(True, 9.50, "1"),
                                           (True, 0.05, "3")]

        mock_custom_site_scraper.side_effect = [True]


        # Populating database, with UserProduct data formatted as:
        # (Name, supplier, stock, price, ID, url, nickname)
        product_data = [self.product_2]
        self.create_user_products(product_data)

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='2').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, UserProduct.objects.all())

        # Grabbing full object and testing for changes
        best_buy_object = Product.objects.get(product_name='2')
        self.assertFalse(best_buy_object.current_stock, "Update to product should have changed stock to out-of-stock")
        self.assertNotEqual(best_buy_object.last_updated, original_timestamp,
                            "Updating product should change the timestamp")

    @patch('scraper_service.custom_site_scraper')
    @patch('scraper_service.amazon_scraper')
    @patch('scraper_service.BestBuyScraper')
    def test_update_products_one_amazon(self, mock_best_buy_scraper, mock_amazon_scraper, mock_custom_site_scraper):
        """Updating a list with a single product from Amazon should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_amazon_scraper.side_effect = [(False, 0.05, "3")]
        mock_custom_site_scraper.side_effect = [True]

        # Populating database, with UserProduct data formatted as:
        # (Name, supplier, stock, price, ID, url, nickname)
        product_data = [self.product_3]
        self.create_user_products(product_data)

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='3').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, UserProduct.objects.all())

        # Grabbing full object and testing for changes
        amazon_object = Product.objects.get(product_name='3')
        self.assertFalse(amazon_object.current_stock, "Update to product should have changed stock to out-of-stock")
        self.assertNotEqual(amazon_object.last_updated, original_timestamp,
                            "Updating product should change the timestamp")

    @patch('scraper_service.custom_site_scraper')
    @patch('scraper_service.amazon_scraper')
    @patch('scraper_service.BestBuyScraper')
    def test_update_products_one_custom(self, mock_best_buy_scraper, mock_amazon_scraper, mock_custom_site_scraper):
        """Updating a list with a single product from Amazon should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_amazon_scraper.side_effect = [(False, 0.05, "3")]
        mock_custom_site_scraper.side_effect = [True]

        # Populating database, with UserProduct data formatted as:
        # (Name, supplier, stock, price, ID, url, nickname)
        product_data = [self.product_4]
        self.create_user_products(product_data)

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='4').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, UserProduct.objects.all())

        # Grabbing full object and testing for changes
        custom_object = Product.objects.get(product_name='4')
        self.assertTrue(custom_object.current_stock, "Update to product should have changed site condition to changed")
        self.assertNotEqual(custom_object.last_updated, original_timestamp,
                            "Updating product should change the timestamp")

    @patch('scraper_service.custom_site_scraper')
    @patch('scraper_service.amazon_scraper')
    @patch('scraper_service.BestBuyScraper')
    def test_update_products_small_mixed(self, mock_best_buy_scraper, mock_amazon_scraper, mock_custom_site_scraper):
        """Updating a list with a single product from Best Buy should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_amazon_scraper.side_effect = [(False, 0.05, "3")]
        mock_custom_site_scraper.side_effect = [True]

        # Populating database, with UserProduct data formatted as:
        # (Name, supplier, stock, price, ID, url, nickname)
        product_data = [self.product_2, self.product_3, self.product_4]
        self.create_user_products(product_data)

        # Storing old version of product object's timestamp data
        original_timestamp_BB = Product.objects.get(product_name='2').last_updated
        original_timestamp_amazon = Product.objects.get(product_name='3').last_updated
        original_timestamp_custom = Product.objects.get(product_name='4').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, UserProduct.objects.all())

        # Grabbing full object and testing for changes
        best_buy_object = Product.objects.get(product_name='2')
        amazon_object = Product.objects.get(product_name='3')
        custom_object = Product.objects.get(product_name='4')
        self.assertFalse(best_buy_object.current_stock,
                         "Update to Best Buy product should have changed stock to out-of-stock")
        self.assertNotEqual(best_buy_object.last_updated, original_timestamp_BB,
                            "Updating Best Buy product should change the timestamp")
        self.assertFalse(amazon_object.current_stock,
                         "Update to Amazon product should have changed stock to out-of-stock")
        self.assertNotEqual(amazon_object.last_updated, original_timestamp_amazon,
                            "Updating Amazon product should change the timestamp")
        self.assertTrue(custom_object.current_stock,
                        "Update to custom product should have changed site condition to changed")
        self.assertNotEqual(custom_object.last_updated, original_timestamp_custom,
                            "Updating custom product should change the timestamp")




