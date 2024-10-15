"""
Django custom command to wait for database to be available
"""
from django.core.mangement.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        pass
        self.stdout.write('Waiting for database...')
        self.stdout.write('Database available!')