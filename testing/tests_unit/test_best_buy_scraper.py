from django.test import TestCase
from products.scraper_driver.best_buy_scraper import BestBuyScraper


class BestBuyTestCases(TestCase):

    def test_sold_out(self):
        """A sold-out item from BB returns the expected information"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self,"https://www.bestbuy.com/site/cookie-dvd-1989"
                                                                 "/18959412.p?skuId=18959412")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "Sold-out item's price not correct")
        self.assertFalse(in_stock, "Sold-out item appears in-stock")
        # Ideally this data should still be returned when an item's listing exists
        # self.assertIn("Cookie", name, "Out-of-stock item's name not found: ")

    def test_high_demand(self):
        """A high-demand (backordered) item from BB returns the expected information"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self,"https://www.bestbuy.com/site/gigabyte-nvidia"
                                                                      "-geforce-rtx-3080-ti-aorus-master-12gb-gddr6x"
                                                                      "-pci-express-4-0-graphics-card/6468932.p?skuId"
                                                                      "=6468932")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "High-demand backordered item's price not correct")
        self.assertFalse(in_stock, "High-demand backordered item appears in-stock")
        # Ideally this data should still be returned when an item's listing exists
        # self.assertIn("3080", name, "High-demand backordered item's name not found: ")

    def test_in_stock(self):
        """An in-stock item from BB returns the expected information"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self, "https://www.bestbuy.com/site/sony-zx-series"
                                                                       "-wired-on-ear-headphones-black/8618232.p"
                                                                       "?skuId=8618232")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 9.99, "Sold-out item's price not correct")
        self.assertTrue(in_stock, "Sold-out item appears in-stock")
        self.assertIn("ZX", name, "Out-of-stock item's name not found: ")

    def test_invalid_link(self):
        """An invalid BB link results in a graceful failure with no uncaught errors"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self, "bestbuy.com/8618232")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "Invalid link should produce a price of 0")
        self.assertFalse(in_stock, "Invalid item appears in-stock")

    def test_non_amazon_site(self):
        """A site other than BB should not cause uncaught errors"""
        in_stock, price, name = BestBuyScraper.get_price_bestbuy(self, "https://www.aliexpress.com/item/32958852196.html")
        # Yes I know aliexpress sucks, I was looking for a site with a vaguely Best Buy-like format

        self.assertEqual(price, 0, "A non-BB site should not have a price returned")
        self.assertFalse(in_stock, "A non-BB site should not be considered in-stock")
        # Exact implementation of naming aspect is up for debate, should probably be an empty string

    def test_get_url_valid(self):
        """A valid SKU should generate the correct BB product link"""
        url = BestBuyScraper.get_product_url_bestbuy(self, "8618232")
        # Using the Sony headphones as the reference point

        self.assertEqual(url, "https://www.bestbuy.com/site/sony-zx-series-wired-on-ear-headphones-black/8618232.p"
                              "?skuId=8618232", "Product URL incorrect")

    def test_get_url_invalid(self):
        """An invalid SKU should not cause uncaught errors"""
        # In this case, our return value isn't particularly well-defined (we'll use an empty string)
        # The key thing is that the failure is graceful, currently testing for no uncaught exceptions.
        # In future, we may want this to throw a specific exception and handle it elsewhere.
        url = BestBuyScraper.get_product_url_bestbuy(self, "861823")
        self.assertEqual(url, '', "Need to test some sort of return value, currently going with it being empty")
