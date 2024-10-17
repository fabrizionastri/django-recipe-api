""" Serializers for the user api view """

from django.contrib.auth import (
    get_user_model,
    authenticate
)                                                                           # import the get_user_model and authenticate functions from the django.contrib.auth module
from rest_framework import serializers                                      # import the serializers module, which is a part of the rest_framework package to serialize and deserialize data. Converts between JSON and Python data types or a model instance in our database
from django.utils.translation import ugettext_lazy as _                     # import the ugettext_lazy function from the django.utils.translation module to translate the strings in the serializer

class UserSerializer(serializers.ModelSerializer):                          # create a UserSerializer class that inherits from the ModelSerializer class. The ModelSerializer class is a class provided by the Django REST framework that automatically generates a serializer class based on the model class that we provide. It allows us to validate and save data to the database according to the model class that we provide
    """ Serializer for the user object """

    class Meta:                                                             # Meta data is used to tell Django which model the serializer is going to be used for, and the fields that are required in the request to create a user
        model = get_user_model()                                            # set the model to the user model. This specifies which model the serializer is going to use
        fields = ('email', 'password', 'name')                              # set the fields that must be provided in the request to create a user and will be passed to the model. Only the values that a user can set themselves should be included in this list (not the is_staff or is_superuser fields)"""  """
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # set the password field to write only and a minimum length of 5. The user can write to the password field but it will not be returned in the response

    def create(self, validated_data):                                       # create a create method to create a new user. Validated data is the data that has been validated by the serializer
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)       # we override the create method to create a new user with the validated data. The create_user method is a custom method that we created in the user model to create a new user with an encrypted password

    def update(self, instance, validated_data):                             # create an update method to update the user
        """ Update a user, setting the password correctly and return it """
        password = validated_data.pop('password', None)                     # get the password from the validated data, and remove it from the validated data. If the password does not exist, set it to None
        user = super().update(instance, validated_data)                     # call the update method of the parent class to update the user
        if password:                                                        # if the password exists
            user.set_password(password)                                      # set the password
            user.save()                                                     # save the user
        return user                                                         # return the user

class AuthTokenSerializer(serializers.Serializer):                          # create a AuthTokenSerializer class that inherits from the basic Serializer class. The Serializer class is a class provided by the Django REST framework that allows us to validate and save data to the database
    """ Serializer for the user authentication token """

    email = serializers.EmailField()                                         # create a CharField for the email
    password = serializers.CharField(                                        # create a CharField for the password
        style={'input_type': 'password'},                                    # set the style to input_type password
        trim_whitespace=False                                                # set trim_whitespace to False to allow for leading and trailing whitespace in the password
    )

    def validate(self, attrs):                                              # create a validate method to validate the email and password. attrs is the attributes that are passed to the serializer, as a dictionary
        """ Validate and authenticate the user """
        email = attrs.get('email')                                          # get the email from the attributes
        password = attrs.get('password')                                    # get the password from the attributes

        user = authenticate(                                                # built-in Django function to authenticate the user
            request=self.context.get('request'),                            # get the request from the context, not really used, but required for the authenticate function
            username=email,
            password=password
        )
        if not user:                                                        # if the user is not authenticated
            msg = _('Unable to authenticate with the provided credentials')     # set the message to 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')    # raise a validation error with the message and code 'authentication'

        attrs['user'] = user                                                # set the user in the attributes
        return attrs                                                        # return the attributes from the validate method