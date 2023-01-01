from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'player/index.html')

def albums_store(request):
    return render(request, 'player/albums-store.html')

def blog(request):
    return render(request, 'player/blog.html')

def contact(request):
    return render(request, 'player/contact.html')

def elements(request):
    return render(request, 'player/elements.html')

def event(request):
    return render(request, 'player/event.html')

