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
        self.assertIsNone(user.discord)

    def test_create_full_user(self):
        user = User.objects.create_user(username='testuser1',
                                        first_name='testfirstname',
                                        last_name='testlastname',
                                        email='testemail',
                                        phone='1234567890',
                                        discord='test#1234',
                                        password='testpassword1')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, 'testuser1'),
        self.assertEqual(user.first_name, 'testfirstname')
        self.assertEqual(user.last_name, 'testlastname')
        self.assertEqual(user.email, 'testemail')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.discord, 'test#1234')
