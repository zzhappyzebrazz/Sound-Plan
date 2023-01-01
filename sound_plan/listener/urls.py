from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from listener.views import *

app_name = 'listener'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('my-account/', my_account, name='my_account'),
    path('logout/', logout, name='logout')
]