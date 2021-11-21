from django.test import TestCase

from account.forms import *
from account.models import User

USERNAME = 'testuser1'
INVALID_USERNAME = 'test!invaliduser1'
PASSWORD = 'testpassword1'
FIRST = 'testfirst'
LAST = 'testlast'
EMAIL = 'testemail@test.test'
INVALID_EMAIL = 'testinvalidemail'


# 1. Test valid minimal form creation
# 2. Test invalid email address
# 3. Test invalid username
# 4. Test missing username
# 5. Test missing other required fields
# 6. Test valid full form creation
# 7. Test invalid phone field
# 8. Test invalid discord
# 9. Test valid phone field
# 10. Test valid discord
# 11. Test invalid (short) password
# 12. Test invalid (common) password
# 13. Test invalid (numerical) password
# 14. Test non-matching passwords entered
class CreateUserFormTest(TestCase):

    def setUp(self):
        pass

    def test_valid_create_minimal_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': INVALID_EMAIL,
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_invalid_username_create_form(self):
        data = {'username': INVALID_USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['username'],
                         ['Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'])

    def test_missing_username_create_form(self):
        data = {'username': '',
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_missing_multiple_fields_create_form(self):
        data = {'username': USERNAME,
                'first_name': '',
                'last_name': '',
                'email': '',
                'password1': '',
                'password2': ''}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_valid_full_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'phone': '1234567890',
                'discord': 'test#1234',
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'phone': '123456789',
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['phone'], ['Please enter a valid phone number'])

    def test_invalid_discord_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test',
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['discord'], ['Discord ID must be in the format string#1234'])

    def test_valid_phone_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'phone': '1234567890',
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_discord_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test#1234',
                'password1': PASSWORD,
                'password2': PASSWORD}
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_short_password_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test#1234',
                'password1': 'short',
                'password2': 'short'}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['password2'], ['This password is too short. It must contain at least 8 characters.'])

    def test_invalid_common_password_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test#1234',
                'password1': 'password',
                'password2': 'password'}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['password2'], ['This password is too common.'])

    def test_invalid_numerical_password_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test#1234',
                'password1': '98273640',
                'password2': '98273640'}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['password2'], ['This password is entirely numeric.'])

    def test_different_password_create_form(self):
        data = {'username': USERNAME,
                'first_name': FIRST,
                'last_name': LAST,
                'email': EMAIL,
                'discord': 'test#1234',
                'password1': 'testpassword1',
                'password2': 'testpassword2'}
        form = CreateUserForm(data=data)
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])


# 1. Test valid login form
# 2. Test invalid login form
class LogInFormTest(TestCase):

    def setUp(self):
        pass

    def test_valid_login_form(self):
        data = {'username': USERNAME, 'password': PASSWORD}
        form = LogInForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {'username': '', 'password': PASSWORD}
        form = LogInForm(data=data)
        self.assertFalse(form.is_valid())


class AccountManagementFormTest(TestCase):

    def setUp(self):
        pass
