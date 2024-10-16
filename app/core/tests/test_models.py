""" Tests for models """

from django.test import TestCase                             # Base class for testing Django applications
from django.contrib.auth import get_user_model               # function to get the default user model for the project, if allows you to get the user model that is active in the current project, even if you change the user model in the future. It is a good practice to use this function to get the user model, instead of importing the user model directly

from decimal import Decimal as Dec
from core import models

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

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized """
        print('test_new_user_email_normalized')
        sample_emails = [
            [ 'test1@EXAMPLE.com', 'test1@example.com' ],
            [ 'Test2@EXAMPLE.com', 'Test2@example.com' ],           # As per email standard, the domain part of the email is case-insensitive, but the local part is case-sensitive. However, most email providers treat the local part as case-insensitive as well. Since we don't know which email provider the user is using, we should treat the local part as case-sensitive, and not convert it to lowercase.
            [ 'TEST3@EXAMPLE.com', 'TEST3@example.com' ],
            [ 'test4@example.com', 'test4@example.com'  ],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'pwd123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating user without an email raises error """
        print('test_new_user_without_email_raises_error')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pwd123')

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        print('test_create_new_superuser')
        user = get_user_model().objects.create_superuser('test@example.com', 'pwd123')
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        """ Test creating a new recipe """
        user = get_user_model().objects.create_user('test@example.com', 'pwd123')
        recipe = models.Recipe.objects.create(
            user = user,
            title = 'Sample recipe name',
            time_minutes = 5,
            price  = Dec('5.50'),
            description= 'Sample recipe description'
        )
        self.assertEqual(str(recipe), recipe.title)