""" Views for the recipe api """

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeSerializer


# def index(request):
#     # return HttpResponseForbidden()
#     return RecipeSerializer(Recipe.objects.all().order_by('-id'), many=True)

class RecipeViewSet(viewsets.ModelViewSet):         # ModelViewSet is designed to manage models in the database
    """ View for manage reipe APIs."""              # This view will offer multiple endpoints for the Recipe model (list, create, update, delete)
    serializer_class = RecipeSerializer             # serializer_class is the serializer class that this view set will use to serialize and deserialize the data
    queryset = Recipe.objects.all()                 # queryset is the list of objects that this view set has access to
    authentication_classes = (TokenAuthentication,) # authentication_classes is the list of authentication classes that this view set will use to authenticate the user → we used TokenAuthentication to authenticate the user with the token that is provided in the request
    permission_classes = (IsAuthenticated,)         # permission_classes is the list of permission classes that this view set will use to check the permissions of the user → users need to be authenticated to access this view

    def get_queryset(self):                         # we need to override the built-in get_queryset method to filter the queryset based on the authenticated user
        """ Retrieve the recipes for the authenticated user """
        self.get_queryset
        return self.queryset.filter(user=self.request.user).order_by('-id')

#     def perform_create(self, serializer):           # we need to override the built-in perform_create method to assign the authenticated user to the recipe
#         """ Create a new recipe """
#         serializer.save(user=self.request.user)
