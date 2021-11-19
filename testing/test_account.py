from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from account.models import User
import time


path = 'resources/webdrivers/chromedriver.exe'



class LoginTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path=path)
        cls.user = User.objects.create_user(username='testuser1',
                                            password='testpassword1')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.selenium.quit()
        cls.user.delete()

    def test_correct_login_functional(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.selenium.find_element(By.ID, 'id_username').send_keys('testuser1')
        self.selenium.find_element(By.ID, 'id_password').send_keys('testpassword1')
        self.selenium.find_element(By.XPATH, '//*[@id="container"]/form/button').click()
        signed_in = self.selenium.find_element(By.XPATH, '//*[@id="container"]/div[1]/nav/ul/li[4]').get_attribute("innerHTML")
        self.assertEqual('Signed in as: testuser1', signed_in)
