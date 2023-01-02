from django.db import models
from django.utils import timezone

# Create your models here.
    
class Artist(models.Model):
    artist_name = models.CharField(max_length=264, blank=False)
    event = models.CharField(max_length=20)
    avartar = models.TextField()
    
    def __str__(self):
        return self.artist_name
    

class Album(models.Model):
    album_name = models.CharField(max_length=264, blank=False)
    artists = models.ForeignKey(Artist, on_delete=models.PROTECT, default='')
    album_cover = models.ImageField(upload_to='player/images', default='player/images/album_default_cover.png')
    public_day = models.DateField()
    
    def __str__(self):
        return self.album_name

    class Meta:
        ordering = ['-public_day']           
    
class Song(models.Model):
    song_name = models.CharField(max_length=264, blank=False)
    audio = models.ImageField(upload_to='player/audio', default='player/audio/dummy-audio.mp3')
    artists = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.PROTECT)

    def __str__(self):
        return self.song_name
    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
