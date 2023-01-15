from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]
