""" Tests for user API """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')  # get the url by its name composed, as a the app name + the url name
TOKEN_URL = reverse('user:token')         # get the url by its name composed, as a the app name + the url name
ME_URL = reverse('user:me')               # get the url by its name composed, as a the app name + the url name


def create_user(**params):
    """ Create and return a new user """
    default_user_details = {                    # create a payload
            'email': 'user@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):                                             # Tests for unauthenticated requests
    """ Test the public features of the users API (unauthenticated requests) """

    def setUp(self):
        self.client = APIClient()                                               # create a client

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        response = self.client.post(CREATE_USER_URL, default_user_details)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)         # check if the response status code is 201
        user = get_user_model().objects.get(email=default_user_details['email'])        # get the user from the database
        self.assertTrue(user.check_password(default_user_details['password']))          # check if the password is correct
        self.assertNotIn('password', response.data)                             # check that the password is not in the response

    def test_user_already_exists(self):
        """ Test creating a user that already exists fails """
        create_user(**default_user_details)                                              # create a user in the database with the payload
        response = self.client.post(CREATE_USER_URL, default_user_details)               # simulate a post request with the same payload
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)      # check if the response status code is 400

    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        default_user_details['password'] = 'pw'
        response = self.client.post(CREATE_USER_URL, default_user_details)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     # check if the response status code is 400
        user_exists = get_user_model().objects.filter(email=default_user_details['email']).exists()    # check if the user exists in the database
        self.assertFalse(user_exists)                                            # check that the user does not exist

    def test_create_token_for_user(self):
        """ Test generates token for valid credentials """
        create_user(**default_user_details)                                             # create a user in the database with the payload
        payload = { 'email': default_user_details['email'], 'password': default_user_details['password'] }
        response = self.client.post(TOKEN_URL, payload)                         # simulate a post request with the payload
        self.assertIn('token', response.data)                                   # check that the token is in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)              # check if the response status code is 200

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(**default_user_details)                                             # create a user in the database with the payload
        payload = { 'email': default_user_details['email'], 'password': 'wrong' }
        response = self.client.post(TOKEN_URL, payload)                         # simulate a post request with the payload
        self.assertNotIn('token', response.data)                                # check that the token is not in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     # check if the response status code is 400

    def test_create_token_blank_password(self):
        """ Test that token is not created if password is blank """
        create_user(**default_user_details)                                             # create a user in the database with the payload
        payload = { 'email': default_user_details['email'], 'password': '' }
        response = self.client.post(TOKEN_URL, payload)                         # simulate a post request with the payload
        self.assertNotIn('token', response.data)                                # check that the token is not in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        response = self.client.get(ME_URL)                                      # simulate a get request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):                                            # Tests for authenticated requests

    def setUp(self):
        self.user = create_user(**default_user_details)                                 # create a user in the database with the payload
        self.client = APIClient()                                               # create a client
        self.client.force_authenticate(user=self.user)                          # authenticate the user using the client using the force_authenticate to avoid making real authentication

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        response = self.client.get(ME_URL)                                      # simulate a get request
        self.assertEqual(response.status_code, status.HTTP_200_OK)              # check if the response status code is 200
        self.assertEqual(response.data, {                                       # check if the response data is the user details
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Test that POST is not allowed on the me url """                     # we only allow PUT and PATCH requests on this url because we are updating the user details
        response = self.client.post(ME_URL, {})                                 # simulate a post request
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = { 'name': 'new name', 'password': 'newpassword' }             # create a payload
        response = self.client.patch(ME_URL, payload)                          # simulate a patch request with the payload
        self.user.refresh_from_db()                                             # refresh the user from the database, otherwise the user object will not be updated in the backend
        self.assertEqual(self.user.name, payload['name'])                       # check if the name is updated
        self.assertTrue(self.user.check_password(payload['password']))          # check if the password is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)              # check if the response status code is 200
