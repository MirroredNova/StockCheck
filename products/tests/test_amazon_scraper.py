from django.test import TestCase
from requests.exceptions import MissingSchema
from products.scrapers.amazon_scraper import amazon_scraper


class AmazonTestCases(TestCase):

    def test_out_of_stock(self):
        """An out-of-stock item from Amazon returns the expected information"""
        in_stock, price, name = amazon_scraper("https://www.amazon.com/ASUS-Graphics-DisplayPort-Military-Grade-Certification/dp/B0985VND1G/ref=sr_1_2?keywords=gpu&qid=1639009409&refinements=p_n_availability%3A2661601011&rnid=2661599011&sr=8-2")

        # print("Got: name = %s, price = %f, stock = %s" % (name, price, in_stock))
        self.assertEqual(price, 0, "Out of stock item's price not correct")
        self.assertFalse(in_stock, "Out of stock item appears in-stock")
        # Looking at the implementation, this shouldn't actually be caught, but it'd be nice if it were
        # self.assertIn("SRMS800", name, "Out-of-stock item's name not found: ")

    def test_only_used_in_stock(self):
        """An item available from only a third-party retailer will count as out of stock"""
        in_stock, price, name = amazon_scraper("https://www.amazon.com/dp/B01MTAAMGZ")
        self.assertFalse(in_stock)
        self.assertEqual(price,0)
        self.assertEqual(name,'Ibanez SR400EQM Quilted Maple Electric Bass Guitar Dragon Eye Burst')

    def test_in_stock(self):
        """An item available directly through Amazon returns the expected information"""
        in_stock, price, name = amazon_scraper("https://www.amazon.com/dp/B01N2145N9")

        self.assertEqual(price, 449.99, "Available item price not as expected (may have changed, confirm)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("AF75G", name, "Available item not named as expected")

    def test_foreign_english_amazon_site(self):
        """A link provided from the .co.uk site returns data as expected (currencies handled at some level)"""
        in_stock, price, name = amazon_scraper("https://www.amazon.co.uk/dp/B0002DVDJW")

        self.assertEqual(price, 114.47, "Available item price not as expected (may have changed, in GBP)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("DW5512", name, "Available item not named as expected")

    def test_foreign_german_amazon_site(self):
        """A link provided from the .de site returns data as expected (currencies handled at some level)"""
        in_stock, price, name = amazon_scraper("https://www.amazon.de/dp/B01AHWW382/")

        self.assertEqual(price, 353.00, "Available item price not as expected (may have changed, in EUR)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("305E", name, "Available item not named as expected")

    def test_shortened_amazon_link(self):
        """Amazon provides shortened link forms, an in-stock item accessed from a shortened link should act the same"""
        in_stock, price, name = amazon_scraper("https://amzn.com/dp/B01N2145N9")

        self.assertEqual(price, 449.99, "Available item price not as expected (may have changed, confirm)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("AF75G", name, "Available item not named as expected")

    def test_no_scheme(self):
        """An link provided with no scheme functions as well as one with a scheme"""
        in_stock, price, name = amazon_scraper("www.amazon.com/dp/B01N2145N9")

        self.assertEqual(price, 449.99, "Available item price not as expected (may have changed, confirm)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("AF75G", name, "Available item not named as expected")

    def test_no_scheme_or_prefix(self):
        """An link provided with no scheme or www prefix functions as well as one with those components"""
        in_stock, price, name = amazon_scraper("amazon.com/dp/B01N2145N9")

        self.assertEqual(price, 449.99, "Available item price not as expected (may have changed, confirm)")
        self.assertTrue(in_stock, "Available item not recognized as available")
        self.assertIn("AF75G", name, "Available item not named as expected")

    def test_invalid_amazon_link(self):
        """An invalid (but properly-formatted) link should raise the appropriate exception"""
        url = "https://www.amazon.com/dp/B01N2145N12"
        self.assertRaises(MissingSchema, amazon_scraper, url)

    def test_non_amazon_site(self):
        """A site other than Amazon should raise the appropriate exception"""
        url = "https://www.aliexpress.com/item/32958852196.html"
        # Yes I know aliexpress sucks, I was looking for a site with a vaguely Amazon-like format
        self.assertRaises(MissingSchema, amazon_scraper, url)
