""" Serializers for the user api view """

from django.contrib.auth import get_user_model
from rest_framework import serializers                                      # import the serializers module, which is a part of the rest_framework package to serialize and deserialize data. Converts between JSON and Python data types or a model instance in our database

class UserSerializer(serializers.ModelSerializer):                          # create a UserSerializer class that inherits from the ModelSerializer class. The ModelSerializer class is a class provided by the Django REST framework that automatically generates a serializer class based on the model class that we provide. It allows us to validate and save data to the database according to the model class that we provide
    """ Serializer for the user object """

    class Meta:                                                             # Meta data is used to tell Django which model the serializer is going to be used for, and the fields that are required in the request to create a user
        model = get_user_model()                                            # set the model to the user model. This specifies which model the serializer is going to use
        fields = ('email', 'password', 'name')                              # set the fields that must be provided in the request to create a user and will be passed to the model. Only the values that a user can set themselves should be included in this list (not the is_staff or is_superuser fields)"""  """
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # set the password field to write only and a minimum length of 5. The user can write to the password field but it will not be returned in the response

    def create(self, validated_data):                                       # create a create method to create a new user
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)       # we override the create method to create a new user with the validated data. The create_user method is a custom method that we created in the user model to create a new user with an encrypted password