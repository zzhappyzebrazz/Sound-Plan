from django.contrib import admin
from django.urls import path
from django.urls import path, re_path
from player.views import *

app_name = 'player'

urlpatterns = [
    path('', index, name="index"),
    path('albums-store', albums_store, name="albums-store"),
    path('blog', blog, name="blog"),
    path('contact', contact, name="contact"),
    path('event', event, name="event"),

]