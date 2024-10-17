from django.contrib.auth import get_user_model

def create_user(**params):
    """ Create and return a new user (with default values provided) """
    defaults = {
        'email': 'user@example.com',
        'password': 'password123',
        'name': 'Test User'
    }
    defaults.update(params)
    return get_user_model().objects.create(**defaults)