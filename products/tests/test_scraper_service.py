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

class ScraperServiceTestCases(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ScraperServiceTestCases, cls).setUpClass()
        cls.run_scraper = RunScraper()
        cls.notification_sender = NotificationSender()

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
        mock_amazon_scraper.side_effect = [(True, 9.50, "1"), (True, 0.05, "3")]
        mock_custom_site_scraper.side_effect = [True]

        # Populating database
        Product.objects.create(supplier='Best Buy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now(tz=timezone.utc), product_name='2',
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

        # Populating database
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now(tz=timezone.utc),
                               product_name='3', product_url='nya3.org')

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='3').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

        # Grabbing full object and testing for changes
        amazon_object = Product.objects.get(product_name='3')
        self.assertFalse(amazon_object.current_stock, "Update to product should have changed stock to out-of-stock")
        self.assertNotEqual(amazon_object.last_updated, original_timestamp,
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

        # Populating database
        Product.objects.create(supplier='Custom Site', current_stock=False, current_price=0,
                               product_id='', last_updated=datetime.now(tz=timezone.utc),
                               product_name='4', product_url='nya4.net')

        # Storing old version of product object's timestamp data
        original_timestamp = Product.objects.get(product_name='4').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

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

        # Populating database
        Product.objects.create(supplier='Best Buy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now(tz=timezone.utc), product_name='2',
                               product_url='nya2.net')
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now(tz=timezone.utc),
                               product_name='3', product_url='nya3.org')
        Product.objects.create(supplier='Custom Site', current_stock=False, current_price=0,
                               product_id='', last_updated=datetime.now(tz=timezone.utc),
                               product_name='4', product_url='nya4.net')

        # Storing old version of product object's timestamp data
        original_timestamp_BB = Product.objects.get(product_name='2').last_updated
        original_timestamp_amazon = Product.objects.get(product_name='3').last_updated
        original_timestamp_custom = Product.objects.get(product_name='4').last_updated

        # Running product update
        RunScraper.update_products(self.run_scraper, Product.objects.all())

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

    def fake_update_products(self, products):
        for each in products:
            each.last_updated = datetime.now(tz=timezone.utc)

    @patch('package.module.RunScraper.update_products')
    def test_main_small_mixed(self, mock_update_products):
        """Updating a list with a single product from Best Buy should change stock from true to false"""

        # Setting up mocks
        mock_update_products.side_effect = self.fake_update_products

        # Populating database
        Product.objects.create(supplier='Best Buy', current_stock=True, current_price=42.00, product_id='B012',
                               last_updated=datetime.now(tz=timezone.utc), product_name='2',
                               product_url='nya2.net')
        Product.objects.create(supplier='Amazon', current_stock=True, current_price=0.01,
                               product_id='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234', last_updated=datetime.now(tz=timezone.utc),
                               product_name='3', product_url='nya3.org')
        Product.objects.create(supplier='Custom Site', current_stock=False, current_price=0,
                               product_id='', last_updated=datetime.now(tz=timezone.utc),
                               product_name='4', product_url='nya4.net')
        User.objects.create_user('User', 'a@b.com', '1254NYA')

        UserProduct.objects.create(product=Product.objects.get(product_name='2'),
                                   product_nickname='Two',
                                   username=User.objects.get(username='User'))
        UserProduct.objects.create(product=Product.objects.get(product_name='3'),
                                   product_nickname='Three',
                                   username=User.objects.get(username='User'))
        UserProduct.objects.create(product=Product.objects.get(product_name='4'),
                                   product_nickname='Four',
                                   username=User.objects.get(username='User'))

        # Storing old version of product object's timestamp data
        original_timestamp_BB = Product.objects.get(product_name='2').last_updated
        original_timestamp_amazon = Product.objects.get(product_name='3').last_updated
        original_timestamp_custom = Product.objects.get(product_name='4').last_updated

        # Running product update
        RunScraper.main(self.run_scraper)

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


