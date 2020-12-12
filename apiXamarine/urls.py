from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', home, name='home'),
    path('register', register_user, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('create_observation', create_observation, name='create_observation'),
    path('get_all_observation', get_all_observation, name='get_all_observation'),
    path('get_user_observation', get_user_observation, name='get_user_observation'),
    path('update_observation/<int:pk>', update_observation, name='update_observation'),
    path('delete_observation/<int:pk>', delete_observation, name='delete_observation')
]
