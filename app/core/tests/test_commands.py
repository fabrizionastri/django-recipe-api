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

    def test_wait_for_db_ready(self, patched_check):                         # patch_check is the patched check method
        """ Test waiting for db when db is available. """
        patched_check.return_value = True                                    # we are mocking the return value of the check method to True
        call_command('wait_for_db')                                          # call the command that we are testing
        patched_check.assert_called_once_with(databases=['default'])          # check if the check method was called once with the correct arguments

    @patch('time.sleep')                                                     # patch the time.sleep method, to avoid real delays during the tests. It replaces it with a MagicMock object, with a None return value
    def test_wait_for_db_delay(self, patched_sleep, patched_check):          # patch_check is the patched check method
    # Beware of the order of the arguments. The arguments order corresponds to the order in which the patches are applied, "inside-out" (i.e. starting with the bottom one, going up). So he patched_sleep method is the first argument, and the patch_check method is the second argument
        """ Test waiting for db when getting OperationalError. """
        # The first 2 times, the check method will raise an Psycopg2Error (the database is not available) , the next 3 times, it will raise a OperationalError (from Django, the database server is available but it has not yet setup the test database), and the last time, it will return True
        patched_check.side_effect = [Psycopg2Error]   * 2 + \
            [OperationalError] * 3 + [True
                                      ]

        call_command('wait_for_db')                           # call the command that we are testing

        # check if the check method was called 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

