from django.shortcuts import render
from player.forms import *
from player.models import *
from sound_plan.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.validators import validate_email
import feedparser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from player.serializers import SongSerializers, AlbumSerializers, ArtistSerializers

def paginator(request, all_items, num_of_items_per_page):
    page = request.GET.get('page', 1) # First page
    paginator = Paginator(all_items, num_of_items_per_page) # Number of items per page
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)   
    
    return items


# Create your views here.
def index(request):
    all_artist = Artist.objects.order_by('artist_name')
    new_album = Album.objects.order_by('-public_day')[:12]
    for album in new_album:
        print(album.public_day)
    popular_artist = Artist.objects.order_by('-id')[:7]
    week_top = Album.objects.order_by('public_day')[:5]
    new_hits = []
    new_hits.append(Song.objects.get(id=4))
    new_hits.append(Song.objects.get(id=40))
    new_hits.append(Song.objects.get(id=77))
    new_hits.append(Song.objects.get(id=108))
    new_hits.append(Song.objects.get(id=120))
    new_hits.append(Song.objects.get(id=326))
    new_hits.append(Song.objects.get(id=392))
    print(popular_artist)
    return render(request, 'player/index.html', {
        'all_artist' : all_artist,
        'new_album' : new_album,
        'popular_artist' : popular_artist,
        'week_top' : week_top,
        'new_hits' : new_hits,
    })

def albums_store(request, keyword):
    all_albums = []
    if keyword == 'All':
        all_albums = Album.objects.order_by('-public_day')
    elif keyword == 'Number':
        number = [str(i) for i in range(0,10)]
        for num in number:
            album = Album.objects.filter(album_name__startswith=num)
            if len(album) > 0:
                for temp in album:
                    all_albums.append(temp)
    else:
        all_albums = Album.objects.filter(album_name__startswith=keyword)
        
    num_album_per_page = 8
    albums = paginator(request, all_albums, num_album_per_page)
    print(all_albums)
    return render(request, 'player/albums-store.html', {
        'albums' : albums,
    })

def news(request):
    rss_link = 'https://pitchfork.com/feed/feed-news/rss'
    newsfeed = feedparser.parse(rss_link)
    entries = newsfeed['entries'][:15]
    num_of_news_per_page = 5
    news = paginator(request, entries, num_of_news_per_page)
    print(len(entries))

    return render(request, 'player/news.html', {
        'news' : news,
    })

def contact(request):
    forms = FormContact()
    result = ''
    if request.POST.get('name'):
        print('got contact request')
        forms = FormContact(request.POST, Contact)
        if forms.is_valid():
            print('the form is legit')
            request.POST._mutable = True
            post = forms.save(commit=False)
            post.name = forms.cleaned_data['name']
            post.email = forms.cleaned_data['email']
            post.subject = forms.cleaned_data['subject']
            post.message = forms.cleaned_data['message']
            post.save()

            #Send mail
            content = f'<p>Hi there!! <b>{post.name}</b>,</p>'
            content += '<p>We received your feedback bellow.</p>'
            content += f'<p>{post.message}</p>'
            content += f'<p>Thank you for your feed back.</p>'
            content += f'<p>Regards,</p>'
            content += f'<p>SoundPlan</p>'

            # send_mail(post.subject, content, EMAIL_HOST_USER, [post.email])
            msg = EmailMultiAlternatives(post.subject, content, EMAIL_HOST_USER, [post.email])
            msg.attach_alternative(content, 'text/html')
            print('start send')
            msg.send()
            print('sent')
            result = '''
            <div class="alert alert-success" role="alert">
                Submit successfully! Thank you!
            </div>
            '''
        else:
            result = '''
            <div class="alert alert-danger" role="alert">
                Submit error! Please check again!
            </div>
            '''
    
    return render(request, 'player/contact.html', {
        'forms' : forms,
        'result' : result,
    })

def event(request):
    all_events = Event.objects.order_by('-date')
    
    events_per_page = 4
    events = paginator(request, all_events, events_per_page)
    
    validate_email_result = ''
    
    if request.POST.get('subscribe_mail'):
        email = request.POST.get('subscribe_mail')
        print(email)
        try:
            validate_email(email)
            
            subject = 'Subscribe to SOUND-PLAN Newsletter'
            content = f'<p>Hello from Sound Plan to you!!! <b>{ email }</b>,</p>'
            content += '<p>We are happy to received your welcome and Subscribe to our Newsletter service!</p>'
            content += f'<p>Hope that you wil have a wonderful experienced here with us. And stay up-to-date with the music world.</p>'
            content += f'<p>You will start receiving Newsletter via Registered E-Mail.</p>'
            content += f'<p>Regards</p>'
            content += f'<p>SoundPlan</p>'
            
            # send_mail(post.subject, content, EMAIL_HOST_USER, [post.email])
            msg = EmailMultiAlternatives(subject, content, EMAIL_HOST_USER, [email])
            msg.attach_alternative(content, 'text/html')
            msg.send()

            validate_email_result = '''
            <div class="alert alert-success" role="alert">
                Successful Subscribe to the SoundPlan Newsletter!
            </div>
            '''
        except forms.ValidationError:
            validate_email_result = '''
            <div class="alert alert-danger" role="alert">
                E-Mail is not in Wright Format!
            </div>
            '''
        
    return render(request, 'player/event.html', {
        'events' : events,
        'validate_email_result' : validate_email_result,
    })

def single_album(request, id):
    album = Album.objects.get(id=id)
    all_songs = Song.objects.filter(album_id=album.id)


    songs_per_page = 8
    songs = paginator(request, all_songs, songs_per_page)

    return render(request, 'player/single-album.html', {
        'album' : album,
        'songs' : songs,
    })

def artist(request, id):
    artist = Artist.objects.get(id=id)
    albums = Album.objects.filter(artists_id=id)
    return render (request, 'player/artist.html', {
        'artist' : artist,
        'albums' : albums,
    })
    
# Web service từ rest_framework
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.order_by('song_name')
    serializer_class = SongSerializers
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.order_by('-public_day')
    serializer_class = AlbumSerializers
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.order_by('artist_name')
    serializer_class = ArtistSerializers
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]