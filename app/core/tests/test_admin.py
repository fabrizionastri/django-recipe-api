""" Test the admin page """

from django.test import TestCase                    # test case class to test django apps
from django.contrib.auth import get_user_model      # get the user model
from django.urls import reverse                     # generate urls for django admin page
from django.test import Client                      # client is a dummy web browser


class AdminSiteTests(TestCase):

    def setUp(self):                                # self is a reference to AdminSiteTests class itself
        """ Create user and client """
        self.client = Client()                      # create a Django test client used to simulate a web browser
        self.admin_user = get_user_model().objects.create_superuser(   # create a super user
            email = 'admin@example.com', password = 'password123')
        self.client.force_login(self.admin_user)    # force the authentication of this user for each request we make using the client
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com', password = 'password123', name = 'Test user')

    def test_users_listed(self):
        """ Test that users are listed on user page """
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)             # make a get request to the url

        self.assertContains(response, self.user.name)  # check if the response contains the user name
        self.assertContains(response, self.user.email)

    def test_edit_user_page(self):
        """ Test that the edit user page works """
        url = reverse('admin:core_user_change', args=[self.user.id])    # generate the url for the user edit page
        response = self.client.get(url)                                 # make a get request to the url

        self.assertEqual(response.status_code, 200)                     # check if the response status code is 200

    def create_uder_page(self):
        """ Test that the create user page works """
        url = reverse('admin:core_user_add')                            # generate the url for the user add page
        response = self.client.get(url)                                 # make a get request to the url

        self.assertEqual(response.status_code, 200)                     # check if the response status code is 200