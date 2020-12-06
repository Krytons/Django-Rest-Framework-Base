from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', home, name='home'),
    path('register', register_user, name='register'),
    path('login', obtain_auth_token, name='login')
]
