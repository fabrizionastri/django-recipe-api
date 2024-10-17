""" Test for the recipe API """

from decimal import Decimal as Dec
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import RecipeSerializer
from core.models import Recipe
from core.tests.utils import create_user

# from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):                                              # This allows us to simplify the tests, and avoid repeating code when creating recipes for tests
    """ Create and return a sample recipe """
    defaults = {
            'title': 'Chile con carne',
            'description': 'The best dish in town',
            'time_minutes': 15,
            'price': Dec('5.50'),
            'link' : 'www.myblog.com/my-favourite-dish-123'
        }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)

# class PublicRecipeAPITest(TestCase):
#     """ Test unautenticated API recipe requests """
#
#     def setUp(self):
#         """ Create client """
#         self.client = APIClient()
#
#     def test_aut_required(self):
#         """ Test auth is required to call API """
#         response = self.client.get(RECIPE_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """ Test autenticated API recipe requests """

    def setUp(self):
        """ Create client """
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_get_recipe_list(self):
        """ Test user can get list of all his recipes """
        create_recipe(user=self.user)
        create_recipe(user=self.user, title="Another recipe")
        response = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """ Test only recipes for authenticated user are returned """
        other_user = create_user(email='test2@example.com')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
