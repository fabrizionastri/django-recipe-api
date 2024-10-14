# app/app/tests.py
"""
Sample tests
"""

from django.test import SimpleTestCase
from app.calc import add, substract


class CalcTests(SimpleTestCase):
    """ Sample tests for the calculator app """
    def test_add(self):
        """ Test that two numbers are added together """
        self.assertEqual(add(3, 8), 11)

    def test_substract(self):
        """ Test that values are subtracted and returned """
        self.assertEqual(substract(10, 15), 5)
