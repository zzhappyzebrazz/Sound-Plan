from django.shortcuts import render
from player.forms import *
from player.models import *
from sound_plan.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
import feedparser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

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

def albums_store(request):
    return render(request, 'player/albums-store.html')

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
    return render(request, 'player/event.html')

def single_album(request, id):
    album = Album.objects.get(id=id)
    songs = Song.objects.filter(album_id=album.id)
    print(str(album.public_day))
    print("==================")
    print(songs)
    print("==================")
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