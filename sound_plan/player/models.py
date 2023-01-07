from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
    
class Artist(models.Model):
    artist_name = models.CharField(max_length=264, blank=False)
    avartar = models.ImageField(upload_to='player/images', default='player/image/default.png')
    
    def __str__(self):
        return self.artist_name
    

class Album(models.Model):
    album_name = models.CharField(max_length=264, blank=False)
    artists = models.ForeignKey(Artist, on_delete=models.PROTECT, default='')
    album_cover = models.ImageField(upload_to='player/images', default='player/image/default.png')
    public_day = models.DateField()
    
    def __str__(self):
        return self.album_name

    class Meta:
        ordering = ['-public_day']           
    
class Song(models.Model):
    song_name = models.CharField(max_length=264, blank=False)
    audio = models.ImageField(upload_to='player/audio', default='player/audio/dummy-audio.mp3')
    artists = models.ForeignKey(Artist, on_delete=models.PROTECT, default='')
    album = models.ForeignKey(Album, on_delete=models.PROTECT)

    def __str__(self):
        return self.song_name
    
class Event(models.Model):
    name = models.CharField(max_length=250, blank=False)
    address = models.CharField(max_length=500, blank=False)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='player/images', default='player/image/default.png')
    date = models.DateField()
    price = models.IntegerField()
    artists = models.ManyToManyField(Artist)
    
    def __str__(self):
        return self.name
    
    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
