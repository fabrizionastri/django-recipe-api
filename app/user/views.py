""" Views for the user app """

from rest_framework import (
    generics,                                 # import the generics module from the rest_framework package to create class-based views, which handle the api requests
    authentication,                           # import the authentication module from the rest_framework package to authenticate the user
    permissions                               # import the permissions module from the rest_framework package to check the permissions of the user
)
from rest_framework.authtoken.views import ObtainAuthToken          # import the ObtainAuthToken class from the rest_framework.authtoken.views module to obtain the authentication token
from rest_framework.settings import api_settings                    # import the api_settings from the rest_framework.settings module to get the default renderer classes

from user.serializers import AuthTokenSerializer, UserSerializer

class CreateUserView(generics.CreateAPIView):                       # create a CreateUserView class that inherits from the CreateAPIView class in the generics module
    """ Create a new user in the system """
    serializer_class = UserSerializer                               # set the serializer class to the UserSerializer class that we created


class CreateTokenView(ObtainAuthToken):                             # create a CreateTokenView class that inherits from the ObtainAuthToken class
    """ Create a new auth token for the user """
    serializer_class = AuthTokenSerializer                          # set the serializer class to the AuthTokenSerializer class that we created. We override the default serializer class in the ObtainAuthToken class with our custom serializer class, because we want to use the email field instead of the username field
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES        # set the renderer classes to the default renderer classes in the api_settings. I gives us a nice UI in the browser to test the api


class ManageUserView(generics.RetrieveUpdateAPIView):               # create a ManageUserView class that inherits from the RetrieveUpdateAPIView class provided by the Django framework in the generics module, and is used to retrieve (GET) and update (PATCH, PUT) the authenticated user
    """ Manage the authenticated user """
    serializer_class = UserSerializer                               # set the serializer class to the UserSerializer class that we created
    authentication_classes = (authentication.TokenAuthentication,)  # set the authentication classes to the TokenAuthentication class. This will authenticate the user with the token that is provided in the request
    permission_classes = (permissions.IsAuthenticated,)             # set the permission classes to the IsAuthenticated class. This will check if the user is authenticated before allowing them to access the view. No other permissions are required, because the user can only access their own profile. They cannot access other users' profiles.

    def get_object(self):                                           # create a get_object method to get the user object
        """ Retrieve and return the authenticated user """
        return self.request.user                                    # return the user that is authenticated in the request