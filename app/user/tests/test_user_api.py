""" Tests for user API """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')  # get the url by its name composed, as a the app name + the url name

payload = {                    # create a payload
        'email': 'user@example.com',
        'password': 'password123',
        'name': 'Test User'
    }

def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):                                         # Tests for unauthenticated requests
    """ Test the public features of the users API (unauthenticated requests) """

    def setUp(self):
        self.client = APIClient()                                           # create a client

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)     # check if the response status code is 201
        user = get_user_model().objects.get(email=payload['email'])         # get the user from the database
        self.assertTrue(user.check_password(payload['password']))           # check if the password is correct
        self.assertNotIn('password', response.data)                         # check that the password is not in the response

    def test_user_already_exists(self):
        """ Test creating a user that already exists fails """
        create_user(**payload)                                               # create a user in the database with the payload
        response = self.client.post(CREATE_USER_URL, payload)                # simulate a post request with the same payload

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # check if the response status code is 400

    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        payload['password'] = 'pw'
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if the response status code is 400
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()                                                         # check if the user exists in the database
        self.assertFalse(user_exists)                                      # check that the user does not exist
