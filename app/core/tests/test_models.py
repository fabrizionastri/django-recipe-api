""" Tests for models """

from django.test import TestCase                             # Base class for testing Django applications
from django.contrib.auth import get_user_model               # function to get the default user model for the project, if allows you to get the user model that is active in the current project, even if you change the user model in the future. It is a good practice to use this function to get the user model, instead of importing the user model directly


class ModelTests(TestCase):
    """ Test the user model """

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        print('test_create_user_with_email_successful')
        self.assertEqual(1, 1)
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
