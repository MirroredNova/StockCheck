from django.test import TestCase
from products.scrapers.custom_site_scraper import custom_site_scraper
import requests

class CustomSiteTestCases(TestCase):

    def test_unchanged_basic_no_element(self):
        """An unchanged (relatively basic) site with no element provided returns the expected information"""
        url = 'https://www.nscalesupply.com/atl/atl-locomotiveemdsd7.html'
        xpath = "/html/body/center[2]/table/tbody/tr[4]/td/center/table[2]/tbody/tr[3]/td[6]/font/img"
        element = ''

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_unchanged_basic_with_element(self):
        """An unchanged (relatively basic) site with an element provided returns the expected information"""
        url = 'http://www.metalsmith.co.uk/metals-materials.htm'
        xpath = "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table[8]/tbody/tr[137]/td[3]/div/strong"
        element = '<strong>Temporary unavailable</strong>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_changed_basic_no_element(self):
        """A changed (relatively basic) site with no element provided returns the expected information"""
        url = 'https://www.nscalesupply.com/atl/atl-locomotiveemdsd7.html'
        xpath = "/html/body/center[2]/table/tbody/tr[4]/td/center/table[1]/tbody/tr[2]/td[6]/font/img"
        element = ''

        changed = custom_site_scraper(url, xpath, element)

        self.assertTrue(changed, "Changed site appears unchanged.")

    def test_changed_basic_with_element(self):
        """A changed (relatively basic) site with an element provided returns the expected information"""
        url = 'http://www.metalsmith.co.uk/metals-materials.htm'
        xpath = "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table[8]/tbody/tr[137]/td[3]/div/strong"
        element = '<strong>£26.80</strong>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertTrue(changed, "Changed site appears unchanged.")

    def test_unchanged_fancy_relative_path(self):
        """An unchanged (fancier) site with a relative XPath returns the expected information"""
        url = 'https://www.hampsonhorns.com/all-horns/reynolds-fe01'
        xpath = '//*[@id="flowContent"]/div[1]'
        element = '<div class="product-mark sold-out">sold out</div>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_unchanged_fancy_rooted_path(self):
        """An unchanged (fancier) site with a rooted XPath returns the expected information"""
        url = 'https://reverb.com/item/39804405-buescher-grand-true-tone-trombone-1920s-or-1930s-silver-gold'
        xpath = "/html/body/main/section/div[2]/div/div/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[1]"
        element = '<div class="button button--gray width-100" data-listing-state="true" data-disabled="true">Listing Sold</div>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_changed_fancy_relative_path(self):
        """A changed (fancier) site with a relative XPath returns the expected information"""
        url = 'https://www.hampsonhorns.com/all-horns/selmer-vuillermoz1'
        xpath = '//*[@id="flowContent"]/div[1]'
        element = '<div class="product-mark sold-out">sold out</div>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertTrue(changed, "Changed site appears unchanged.")

    def test_changed_fancy_rooted_path(self):
        """A changed (fancier) site with a rooted XPath returns the expected information"""
        url = 'https://reverb.com/item/38391569-conn-mellophone-eb-d-c-f-made-in-1907'
        xpath = "/html/body/main/section/div[2]/div/div/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[1]"
        element = '<div class="button button--gray width-100" data-listing-state="true" data-disabled="true">Listing Sold</div>'

        changed = custom_site_scraper(url, xpath, element)

        self.assertTrue(changed, "Changed site appears unchanged.")

    def test_no_scheme(self):
        """An link provided with no scheme functions as well as one with a scheme"""
        url = 'www.nscalesupply.com/atl/atl-locomotiveemdsd7.html'
        xpath = "/html/body/center[2]/table/tbody/tr[4]/td/center/table[2]/tbody/tr[3]/td[6]/font/img"
        element = '<img src="../Images/SoldOutOnYellow.gif" width="88" height="20">'

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_no_scheme_or_prefix(self):
        """An link provided with no scheme or www prefix functions as well as one with those components"""
        url = 'nscalesupply.com/atl/atl-locomotiveemdsd7.html'
        xpath = "/html/body/center[2]/table/tbody/tr[4]/td/center/table[2]/tbody/tr[3]/td[6]/font/img"
        element = '<img src="../Images/SoldOutOnYellow.gif" width="88" height="20">'

        changed = custom_site_scraper(url, xpath, element)

        self.assertFalse(changed, "Unchanged site appears changed.")

    def test_multiple_returns(self):
        """An XPath matching multiple elements produces the expected ValueError"""
        url = 'https://www.hampsonhorns.com/all-horns/reynolds-fe01'
        xpath = '//div'
        element = '<div class="product-mark sold-out">sold out</div>'

        self.assertRaises(ValueError, custom_site_scraper, url, xpath, element)

    def test_invalid_link(self):
        """A site returning a 404 error produces the expected HTTPError"""
        url = 'https://www.nscalesupply.com/atl/atl-locomotiveemdsd5.html'
        xpath = "/html/body/center[2]/table/tbody/tr[4]/td/center/table[2]/tbody/tr[3]/td[6]/font/img"
        element = ''

        self.assertRaises(requests.HTTPError, custom_site_scraper, url, xpath, element)