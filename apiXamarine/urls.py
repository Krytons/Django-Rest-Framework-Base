from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', home, name='home'),
    path('register', register_user, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('create_observation', create_observation, name='create_observation'),
    path('get_all_observation', get_all_observation, name='get_all_observation')
]
