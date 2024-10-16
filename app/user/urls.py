""" URL patterns for the user app. """

from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.CreateTokenView.as_view(), name='me'),            # used to update the user's profile
]