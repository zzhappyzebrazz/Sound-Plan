from django.shortcuts import render
from player.forms import *
from player.models import *
from sound_plan.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives

# Create your views here.
def index(request):
    return render(request, 'player/index.html')

def albums_store(request):
    return render(request, 'player/albums-store.html')

def blog(request):
    return render(request, 'player/blog.html')

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
            msg.send()

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

