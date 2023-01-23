from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    path('cart/', cart, name='cart'),
    # path('check-out/', checkout, name='checkout'),
    path('buy-now/<int:event_id>/', buy_now, name='buy_now'),
    path('delete/<int:event_id>/', delete, name='delete'),
]
