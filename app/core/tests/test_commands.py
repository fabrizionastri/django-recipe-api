"""
Test custom management commands
"""

from unittest.mock import patch                         # to mock the behavior of the input function
from psycopg2 import OperationalError as Psycopg2Error  # errors that we could get if the database is not available

from django.core.management import call_command         # to call the command that we are testing
from django.db.utils import OperationalError            # erros that we could get if the database is not available
from django.test import SimpleTestCase                  # the base test case class that we are going to use, we don't need migrations, so we don't need to use TestCase

@patch('core.management.commands.wait_for_db.Command.check')  # patch the check method of the Command class. Check is a method of the BaseCommand class, so we are patching the check method of the BaseCommand class
class CommandTests(SimpleTestCase):
    """ Test commands """

    def test_wait_for_db_ready(self, patched_check):          # patch_check is the patched check method
        """ Test waiting for db when db is available. """
        patched_check.return_value = True                     # we are mocking the return value of the check method to True
        call_command('wait_for_db')                           # call the command that we are testing
        patched_check.assert_called_once_with(database=['default'])   # check if the check method was called with the correct arguments
