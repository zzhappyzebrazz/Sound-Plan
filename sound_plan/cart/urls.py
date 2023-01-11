from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    path('cart/<int:event_id>', cart, name='cart'),
]