"""
Django command to wait for the database to be available.
"""

import time                                              # to add the sleep function
from psycopg2 import OperationalError as Psycopg2Error   # errors that we could get if the database app is not ready
from django.db.utils import OperationalError             # errors that Django throws if the database is not ready
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""
    def handle(self, *args, **options):
        """ Entry point for the command. """
        self.stdout.write('Waiting for database...')    # print a message to the console
        db_up = False                                   # flag to check if the database is up
        while not db_up:                                # while the database is not up
            try:
                self.check(databases=['default'])                            # check if the database is up
                db_up = True                            # if the check method does not raise an error, the database is up
            except (Psycopg2Error):    # if the check method raises an error
                self.stdout.write('Psycopg2Error: Database unavailable, waiting 1 second...')
                time.sleep(1)                            # wait for 1 second
            except (OperationalError):    # if the check method raises an error
                self.stdout.write('OperationalError: Database unavailable, waiting 1 second...')
                time.sleep(1)                            # wait for 1 second
        self.stdout.write(self.style.SUCCESS('Database available!'))
