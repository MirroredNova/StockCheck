from django.test import TestCase
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from products.scrapers.best_buy_scraper import BestBuyScraper
from scraper_service import RunScraper
from scraper_service import NotificationSender
from scraper_service import main
from products.models import Product
from datetime import datetime

class ScraperServiceTestCases(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ScraperServiceTestCases, cls).setUpClass()
        cls.run_scraper = RunScraper()
        cls.notification_sender = NotificationSender()


    def test_create_dict_empty(self):
        """No products in database should not cause uncaught errors"""
        RunScraper.create_product_dict(self.run_scraper)
        # Because I don't know the structure of a product_dict, I can't check if its size is 0

    def test_create_dict_one(self):
        """Only a single product in the database should result in a matching dict"""
        Product.objects.create(supplier='Amazon', current_stock=False, current_price=10.00, product_id=15,
                               last_updated=datetime.now().time(), product_name='1', product_nickname='One',
                               product_url='nya.com')
        # With no return value, I'll start by just running this function and confirming that no errors appear
        RunScraper.create_product_dict(self.run_scraper)

        # Once the product_dict is handled, this should help confirm things
        # object = Product.objects.get(product_name='1')
        # self.assertEqual(RunScraper.product_dict['1'], object.last_updated, "Unexpected value for element in dict")

    def test_create_dict_several(self):
        """Several products in the database should result in a matching dict"""
        Product.objects.create(supplier='Amazon', current_stock=False, current_price=10.00, product_id='15',
                               last_updated=datetime.now().time(), product_name='1', product_nickname='One',
                               product_url='nya.com')
        Product.objects.create(supplier='bestbuy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now().time(), product_name='2', product_nickname='Two',
                               product_url='nya2.net')
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now().time(),
                               product_name='3', product_nickname='Three', product_url='nya3.org')

        # With no return value, I'll start by just running this function and confirming that no errors appear
        RunScraper.create_product_dict(self.run_scraper)

        # Once the product_dict is handled, this should help confirm things
        # an_object = Product.objects.get(product_name='3')
        # self.assertEqual(RunScraper.product_dict['3'], an_object.last_updated, "Unexpected value for element in dict")

    @patch('products.scrapers.scraper_service.amazon_scraper')
    @patch('products.scrapers.scraper_service.BestBuyScraper')
    def test_update_products_empty(self, mock_best_buy_scraper, mock_amazon_scraper):
        """Updating an empty list of products should not cause any uncaught errors"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_BB_class.get_product_url_bestbuy.side_effect = ['nya2.net']
        mock_amazon_scraper.side_effect = [(True, 9.50, "1"), (True, 0.05, "3")]

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

    @patch('products.scrapers.scraper_service.amazon_scraper')
    @patch('products.scrapers.scraper_service.BestBuyScraper')
    def test_update_products_one_best_buy(self, mock_best_buy_scraper, mock_amazon_scraper):
        """Updating a list with a single product from Best Buy should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_BB_class.get_product_url_bestbuy.side_effect = ['nya2.net']
        mock_amazon_scraper.side_effect = [(True, 9.50, "1"), (True, 0.05, "3")]

        # Populating database
        Product.objects.create(supplier='bestbuy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now().time(), product_name='2', product_nickname='Two',
                               product_url='nya2.net')

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='2').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

        # Grabbing full object and testing for changes
        best_buy_object = Product.objects.get(product_name='2')
        self.assertFalse(best_buy_object.current_stock, "Update to product should have changed stock to out-of-stock")
        self.assertNotEqual(best_buy_object.last_updated, original_timestamp,
                            "Updating product should change the timestamp")

    @patch('products.scrapers.scraper_service.amazon_scraper')
    @patch('products.scrapers.scraper_service.BestBuyScraper')
    def test_update_products_one_amazon(self, mock_best_buy_scraper, mock_amazon_scraper):
        """Updating a list with a single product from Amazon should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_BB_class.get_product_url_bestbuy.side_effect = ['nya2.net']
        mock_amazon_scraper.side_effect = [(False, 0.05, "3")]

        # Populating database
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now().time(),
                               product_name='3', product_nickname='Three', product_url='nya3.org')

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='3').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

        # Grabbing full object and testing for changes
        amazon_object = Product.objects.get(product_name='3')
        self.assertFalse(amazon_object.current_stock, "Update to product should have changed stock to out-of-stock")
        self.assertNotEqual(amazon_object.last_updated, original_timestamp,
                            "Updating product should change the timestamp")

    @patch('products.scrapers.scraper_service.amazon_scraper')
    @patch('products.scrapers.scraper_service.BestBuyScraper')
    def test_update_products_small_mixed(self, mock_best_buy_scraper, mock_amazon_scraper):
        """Updating a list with a single product from Best Buy should change stock from true to false"""

        # Setting up mocks
        mock_BB_class = mock_best_buy_scraper.return_value
        mock_BB_class.get_price_bestbuy.side_effect = [(False, 42.00, "2")]
        mock_BB_class.get_product_url_bestbuy.side_effect = ['nya2.net']
        mock_amazon_scraper.side_effect = [(False, 9.50, "1"), (True, 0.05, "3")]

        # Populating database
        Product.objects.create(supplier='bestbuy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now().time(), product_name='2', product_nickname='Two',
                               product_url='nya2.net')
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now().time(),
                               product_name='3', product_nickname='Three', product_url='nya3.org')

        # Storing old version of product object's timestamp data
        original_timestamp_BB = Product.objects.get(product_name='2').last_updated
        original_timestamp_amazon = Product.objects.get(product_name='3').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

        # Grabbing full object and testing for changes
        best_buy_object = Product.objects.get(product_name='2')
        amazon_object = Product.objects.get(product_name='3')
        self.assertFalse(best_buy_object.current_stock,
                         "Update to Best Buy product should have changed stock to out-of-stock")
        self.assertNotEqual(best_buy_object.last_updated, original_timestamp_BB,
                            "Updating Best Buy product should change the timestamp")
        self.assertFalse(amazon_object.current_stock,
                         "Update to Amazon product should have changed stock to out-of-stock")
        self.assertNotEqual(amazon_object.last_updated, original_timestamp_amazon,
                            "Updating Amazon product should change the timestamp")
