# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.common.keys import Keys
# from account.models import User
# import time
#
#
# path = 'resources/webdrivers/chromedriver.exe'
# TEST_USERNAME = 'testuser1'
# TEST_PASSWORD = 'testpassword1'
#
#
# class LoginTest(StaticLiveServerTestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = webdriver.Chrome(executable_path=path)
#
#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.selenium.quit()
#
#     def setUp(self):
#         super(LoginTest, self).setUp()
#
#     def test_correct_register_success(self):
#         pass
