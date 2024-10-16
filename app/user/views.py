""" Views for the user app """

from rest_framework import generics                     # import the generics module from the rest_framework package to create class-based views, which handle the api requests

from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):            # create a CreateUserView class that inherits from the CreateAPIView class in the generics module
    """ Create a new user in the system """
    serializer_class = UserSerializer                    # set the serializer class to the UserSerializer class that we created