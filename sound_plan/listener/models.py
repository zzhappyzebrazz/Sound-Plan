from django.db import models
from player.models import Song

# Create your models here.
class Listener(models.Model):
    first_name = models.CharField(max_length=264, blank=False)
    last_name = models.CharField(max_length=264, blank=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    playlist = models.ForeignKey('Playlist', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Playlist(models.Model):
    playlist_name = models.CharField(max_length=50, blank=False)
    # listener = models.ForeignKey(Listener, on_delete=models.PROTECT)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.playlist_name
    
class ListenerProfileInfo(models.Model):
    #Create relationship from this class to Listener
    listener = models.OneToOneField(Listener, on_delete=models.PROTECT)
    #Add attributes
    portfolio = models.URLField(blank=True)
    image = models.ImageField(upload_to="player/listener/", default="player/listener/avatar_default.jpg")
    
    def __str__(self):
        return self.listener