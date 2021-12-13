from django.test import TestCase
import sys
from products.scrapers.best_buy_scraper import BestBuyScraper
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException

class BestBuyTestCases(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BestBuyTestCases, cls).setUpClass()
        cls.scraper = BestBuyScraper()

    def test_sold_out(self):
        """A sold-out item from BB returns the expected information"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self.scraper,"https://www.bestbuy.com/site/cookie-dvd-1989"
                                                                 "/18959412.p?skuId=18959412")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "Sold-out item's price not correct")
        self.assertFalse(in_stock, "Sold-out item appears in-stock")
        # Ideally this data should still be returned when an item's listing exists
        # self.assertIn("Cookie", name, "Out-of-stock item's name not found: ")

    def test_high_demand(self):
        """A high-demand (backordered) item from BB returns the expected information"""
        url = "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3080-ti-aorus-master-12gb-gddr6x-pci-express-4-0-graphics-card/6468932.p?skuId=6468932"
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self.scraper,url)

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "High-demand backordered item's price not correct")
        self.assertFalse(in_stock, "High-demand backordered item appears in-stock")
        # Ideally this data should still be returned when an item's listing exists
        # self.assertIn("3080", name, "High-demand backordered item's name not found: ")

    def test_in_stock(self):
        """An in-stock item from BB returns the expected information"""
        url = "https://www.bestbuy.com/site/sony-zx-series-wired-on-ear-headphones-black/8618232.p?skuId=8618232"
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self.scraper, url)

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 9.99, "Sold-out item's price not correct")
        self.assertTrue(in_stock, "Sold-out item appears in-stock")
        self.assertIn("ZX", name, "Out-of-stock item's name not found: ")

    def test_no_scheme(self):
        """An link provided with no scheme functions as well as one with a scheme"""
        url = "www.bestbuy.com/site/sony-zx-series-wired-on-ear-headphones-black/8618232.p?skuId=8618232"
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self.scraper, url)

        self.assertEqual(price, 9.99, "Sold-out item's price not correct")
        self.assertTrue(in_stock, "Sold-out item appears in-stock")
        self.assertIn("ZX", name, "Out-of-stock item's name not found: ")

    def test_no_scheme_or_prefix(self):
        """An link provided with no scheme or www prefix functions as well as one with those components"""
        url = "bestbuy.com/site/sony-zx-series-wired-on-ear-headphones-black/8618232.p?skuId=8618232"
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self.scraper, url)

        self.assertEqual(price, 9.99, "Sold-out item's price not correct")
        self.assertTrue(in_stock, "Sold-out item appears in-stock")
        self.assertIn("ZX", name, "Out-of-stock item's name not found: ")

    def test_non_best_buy_site(self):
        """A site other than BB should throw a NoSuchElementException """
        # Yes I know aliexpress sucks, I was looking for a site with a vaguely Best Buy-like format
        self.assertRaises(NoSuchElementException,self.scraper.get_price_bestbuy, "https://www.aliexpress.com/item/32958852196.html")
        
        # Exact implementation of naming aspect is up for debate, should probably be an empty string

    def test_invalid_link(self):
        """An invalid BB link results in a graceful failure with no uncaught errors"""
        self.assertRaises(InvalidArgumentException, self.scraper.get_price_bestbuy, 'https://www.bestbuy.com/8618232')

    