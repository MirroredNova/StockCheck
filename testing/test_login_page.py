from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from StockCheck.settings import CHROMEDRIVER_PATH
from account.models import User
import time


TEST_USERNAME = 'testuser1'
TEST_PASSWORD = 'testpassword1'


class LoginTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.selenium.quit()

    def setUp(self):
        super(LoginTest, self).setUp()
        self.user = User.objects.create_user(username=TEST_USERNAME,
                                             password=TEST_PASSWORD)

    def tearDown(self):
        self.user.delete()

    def test_correct_login_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.selenium.find_element(By.ID, 'id_username').send_keys(TEST_USERNAME)
        self.selenium.find_element(By.ID, 'id_password').send_keys(TEST_PASSWORD)
        self.selenium.find_element(By.XPATH, '//*[@id="container"]/form/button').click()
        signed_in = self.selenium.find_element(By.XPATH, '//*[@id="container"]/div[1]/nav/ul/li[4]').get_attribute("innerHTML")
        self.assertEqual('Signed in as: testuser1', signed_in)

    def test_bad_login_fail(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.selenium.find_element(By.ID, 'id_username').send_keys(TEST_USERNAME)
        self.selenium.find_element(By.ID, 'id_password').send_keys('bad_password')
        self.selenium.find_element(By.XPATH, '//*[@id="container"]/form/button').click()
        failed_message = self.selenium.find_element(By.XPATH, '//*[@id="container"]/ul/li').get_attribute("innerHTML")
        self.assertEqual("That user doesn't exist or the password is incorrect.", failed_message)

    def test_missing_login_info_fail(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.selenium.find_element(By.ID, 'id_username').send_keys(TEST_USERNAME)
        self.selenium.find_element(By.ID, 'id_password').send_keys('')
        self.selenium.find_element(By.XPATH, '//*[@id="container"]/form/button').click()
        self.assertTrue(self.selenium.find_element(By.ID, 'id_username').is_displayed())

    def test_login_form_fields_visible(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.assertTrue(self.selenium.find_element(By.ID, 'id_username').is_displayed())
        self.assertTrue(self.selenium.find_element(By.ID, 'id_password').is_displayed())
        self.assertTrue(self.selenium.find_element(By.XPATH, '//*[@id="container"]/form/button').is_displayed())

    def test_login_links_visible(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.assertTrue(self.selenium.find_element(By.XPATH, '//*[@id="container"]/a[1]').is_displayed())
        self.assertTrue(self.selenium.find_element(By.XPATH, '//*[@id="container"]/a[2]').is_displayed())
