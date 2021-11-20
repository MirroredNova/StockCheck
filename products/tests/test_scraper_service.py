from django.test import TestCase
from products.scrapers.scraper_service import RunScraper
from products.scrapers.scraper_service import NotificationSender
from products.scrapers.scraper_service import main
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

    def test_create_dict_one(self):
        """Only a single product in the database should result in a matching dict"""
        Product.objects.create(supplier='Amazon', current_stock=False, current_price=10.00, product_id='15',
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
        # object = Product.objects.get(product_name='3')
        # self.assertEqual(RunScraper.product_dict['3'], object.last_updated, "Unexpected value for element in dict")
