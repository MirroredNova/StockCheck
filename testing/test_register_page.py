from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from account.models import User
import time
from StockCheck.settings import CHROMEDRIVER_PATH

TEST_USERNAME = 'testuser1'
TEST_PASSWORD = 'testpassword1'


class LoginTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('log-level=3')
        cls.selenium = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=options)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.selenium.quit()

    def setUp(self):
        super(LoginTest, self).setUp()

    def test_correct_register_success(self):
        pass
