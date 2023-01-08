from django.contrib import admin
from listener.models import *
from player.models import *

# Register your models here.
admin.site.register(Listener)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Event)