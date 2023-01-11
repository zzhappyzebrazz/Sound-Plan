from django.shortcuts import render

# Create your views here.
def cart(request, event_id):
    
    return render(request, 'player/cart.html')