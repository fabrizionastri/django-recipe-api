# from django.urls import path, include
from .views import RecipeViewSet

from rest_framework.routers import DefaultRouter   # allows us to generate all the default urls automatically from an built-in API view set

router = DefaultRouter()                        # default router automatically generates all the urls depending on the functionalities that we add have added to the view set (list, create, update, delete).
router.register('recipe', RecipeViewSet)        # register the RecipeViewSet with the router under the name 'recipe'. Assigns the auto-generated urls to the 'recipe' name

app_name = 'recipe'                             # set the app name to 'recipe'. This is used to identify the app in the urls.py file in the project folder. This is the name we will use when we use the reverse function to generate the urls


# Solution 1 - use the router.urls to get automatically generated urls
urlpatterns = router.urls

# Solution 2 - use the include function to include the router.urls
# urlpatterns = [
#     path('', include(router.urls)),
# ]
#
# Solution 3 - manually define the urls one by one
# urlpatterns = [
#     # path('recipe-list/', RecipeViewSet.as_view({'get': 'list'}), name='recipe-list')
# ]
