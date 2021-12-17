from django.test import TestCase

# Create your tests here.
from account.models import User


class UserTest(TestCase):

    def setUp(self):
        pass

    def test_create_minimal_user(self):
        user = User.objects.create_user(username='testuser1', password='testpassword1')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, 'testuser1')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.email, '')
        self.assertIsNone(user.phone)
        self.assertIsNone(user.discord_webhook_url)

    def test_create_full_user(self):
        user = User.objects.create_user(username='testuser1',
                                        first_name='testfirstname',
                                        last_name='testlastname',
                                        email='testemail',
                                        phone='1234567890',
                                        discord_webhook_url='https://discord.com/api/webhooks/920043553957216296/DrQpUJo8zDSodoSHmG05vBUGZKPnlEP9UDny9ChPSGfXsJjK4enJNmxIxZYWCX7mvtqF',
                                        password='testpassword1')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, 'testuser1'),
        self.assertEqual(user.first_name, 'testfirstname')
        self.assertEqual(user.last_name, 'testlastname')
        self.assertEqual(user.email, 'testemail')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.discord_webhook_url, 'https://discord.com/api/webhooks/920043553957216296/DrQpUJo8zDSodoSHmG05vBUGZKPnlEP9UDny9ChPSGfXsJjK4enJNmxIxZYWCX7mvtqF')
