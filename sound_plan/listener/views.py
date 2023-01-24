
from django.shortcuts import render, redirect
from listener.forms import *
from listener.models import Listener, Playlist
from sound_plan.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from cart.models import Order, OrderItem
from player.models import Event, Song
from django.core.validators import validate_email
from random import choice
import string

hasher = PBKDF2PasswordHasher()

# Create your views here.
def login(request):
    print('###LOGIN###')
    # Check login status before
    if 's_user' in request.session:
        return redirect('player:index')

    forms = FormLogin()
    login_email = ''
    password = ''
    #EXECUTE LOGIN
    headline1 = "See what’s new"
    headline2 = "Login"
    result_login = ''
    if request.POST.get('email'):
        forms = FormLogin(request.POST)
        if forms.is_valid():
            print('Get valid POST from LOGIN')
            login_email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
        print(forms)
        print('=====================')
        print(login_email)
        print(password)
        print(hasher.encode(password, 'magic string'))
        print('=====================')
        query = Listener.objects.filter(email=login_email, password=hasher.encode(password, 'magic string'))
        print(query)
        if query.count() > 0:
            print(type(query))
            dict_user = query.values()[0]
            print(type(query.values()))
            print(type(dict_user))
            print(dict_user)
            del(dict_user['password'])
            print(dict_user)
            #if login success the session 's_user' will be saved
            request.session['s_user'] = dict_user
            result_login = '''
                    <div class="alert alert-success" role="alert">
                        Login Success!
                    </div>
                    '''
            return redirect('player:index')
        else:
            result_login = '''
                    <div class="alert alert-danger" role="alert">
                        Login Failed!
                    </div>
                    '''
    return render(request, 'player/login.html', {
        'headline1' : headline1,
        'headline2' : headline2,
        'forms' : forms,
        'result_login' : result_login,
    })

def register(request):
    is_register = True
    print('###REGISTER###')
    #EXECUTE REGISTER
    headline1 = "Let's Explore"
    headline2 = "Register"
    forms = FormRegister()
    result_register = ''

    if request.POST.get('first_name'):
        forms = FormRegister(request.POST, Listener)
        if forms.is_valid():
            print('Get valid POST from REGISTER')
            if forms.cleaned_data['password'] == forms.cleaned_data['confirm_password']:
                request.POST._mutable = True
                post = forms.save(commit=False)
                post.first_name = forms.cleaned_data['first_name']
                post.last_name = forms.cleaned_data['last_name']
                post.email = forms.cleaned_data['email']
                post.password = hasher.encode(forms.cleaned_data['password'], 'magic string')
                #<algorithm>$<iterations>$<salt>$<hash>
                post.phone = forms.cleaned_data['phone']
                post.address = forms.cleaned_data['address']
                post.save()

                #Send mail successful Registered
                subject = 'Sound Plan Registration Success'
                user_name = str(post.first_name) + ' ' + str(post.last_name)
                print("Successful Registered")
                content = f'<p>Hello from Sound Plan to you!!! <b>{ user_name }</b>,</p>'
                content += '<p>We are happy to have you on our journey</p>'
                content += f'<p>Hope that you wil have a wonderful experienced here with us. Stay tuned for more exciting music.</p>'
                content += f'<p>Regards</p>'
                content += f'<p>SoundPlan</p>'

                # send_mail(post.subject, content, EMAIL_HOST_USER, [post.email])
                msg = EmailMultiAlternatives(subject, content, EMAIL_HOST_USER, [post.email])
                msg.attach_alternative(content, 'text/html')
                msg.send()

                result_register = '''
                    <div class="alert alert-success" role="alert">
                        Register Success!
                    </div>
                    '''
                return redirect('listener:login')
            else:
                print('CONFIRM PASSWORD NOT MATCH')
                result_register = '''
                        <div class="alert alert-danger" role="alert">
                            Confirm password not match!
                        </div>
                        '''
    
        else:
            print(forms)
            result_register = '''
            <div class="alert alert-danger" role="alert">
                Invalid!!!
            </div>
            '''
    
    return render(request, 'player/login.html', {
        'is_register' : is_register,
        'headline1' : headline1,
        'headline2' : headline2,
        'forms' : forms,
        'result_register' : result_register,
        
    })
    
def my_account(request):
    
    if 's_user' not in request.session:
        print('User un-registered')
        return redirect('player:index')
    
    # Show user information CHECK
    user = request.session['s_user']
    print(user)

    info_forms = FormUpdateInfo(initial={
        'first_name' : user['first_name'],
        'last_name' : user['last_name'],
        'phone' : user['phone'],
        'address' : user['address'],
    })
            
    # Update user information
    result_update_info = ''
    user_data = Listener.objects.get(id=user['id'])
    print(user_data.password)
    if request.POST.get('first_name'):
        info_forms = FormUpdateInfo(request.POST)
        if info_forms.is_valid():
            print('Get valid POST from UPDATE')
            # request.POST._mutable = True
            # post = forms.save(commit=False)
            first_name = info_forms.cleaned_data['first_name']
            last_name = info_forms.cleaned_data['last_name']
            phone = info_forms.cleaned_data['phone']
            address = info_forms.cleaned_data['address']
            
            user_data.first_name = first_name
            user_data.last_name = last_name
            user_data.phone = phone
            user_data.address = address
            
            user_data.save()
            
            #Update to session
            user['first_name'] = first_name
            user['last_name'] = last_name
            user['phone'] = phone
            user['address'] = address
            request.session['s_user'] = user            
            print(user)
            result_update_info = '''
                <div class="alert alert-success" role="alert">
                    Update User profile Success!!!
                </div>
                '''
        else:
            result_update_info = '''
                <div class="alert alert-danger" role="alert">
                    Please Fill out the Form!!!
                </div>
            '''
    
    # Change password
    result_change_password = ''
    password_forms = FormUserChangePassword()

    if request.POST.get('old_password'):
        password_forms = FormUserChangePassword(request.POST)
        print(password_forms.errors)
        if password_forms.is_valid():
            print('Get valid POST from Change')
            
            old_password = hasher.encode(password_forms.cleaned_data['old_password'], 'magic string')
            new_password = hasher.encode(password_forms.cleaned_data['new_password'], 'magic string')
            confirm_password = hasher.encode(password_forms.cleaned_data['confirm_password'], 'magic string')
            if old_password == user_data.password:
                if new_password == confirm_password:
                    user_data.password = new_password
                    user_data.save()
                    result_change_password = '''
                    <div class="alert alert-success" role="alert">
                        Password Updated!!!
                    </div>
                    '''
                    # return redirect('listener:logout')
                else:
                    result_change_password = '''
                    <div class="alert alert-danger" role="alert">
                        Confirm Password Not Match!!!
                    </div>
                    '''
            else:
                result_change_password = '''
                <div class="alert alert-danger" role="alert">
                    Old Password Incorrect!!!
                </div>
                '''

        else:
            result_change_password = '''
                <div class="alert alert-danger" role="alert">
                    Please Fill out the Form!!!
                </div>
            '''
                
    #Show user order history
    orders = Order.objects.filter(listener_id=user['id']).order_by('-created')
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order=order.id).values())
        for order_item in order_items:
            event = Event.objects.get(pk=order_item['event_id'])
            order_item['event_name'] = event.name
            order_item['total_price'] = order.total
        else:
            dict_order_items = {
                order.pk: order_items
            }
            dict_orders.update(dict_order_items)    
    
    #Show user Play list
    user_playlist = Playlist.objects.filter(listener_id=user_data.id)
    playlist = Playlist()
    if user_playlist.count() > 0:
        playlist_id = user_playlist.values()[0]
        playlist = Playlist.objects.get(id=playlist_id['id'])
        playlist_songs = playlist.songs.all()
    else:
        print(user_playlist)
        
    if request.method == 'POST':
        song_id = int(request.POST.get('remove'))
        if song_id > 0:
            song = Song.objects.get(id=song_id)
            playlist.songs.remove(song)
    
    return render(request, 'player/my-account.html', {
        'user' : user,
        'info_forms' : info_forms,
        'password_forms' : password_forms,
        'result_update_info' : result_update_info,
        'result_change_password' : result_change_password,
        'dict_orders' : dict_orders,
        'orders' : orders,
        'playlist_songs' : playlist_songs,
    })

def logout(request):
    if 's_user' in request.session:
        del request.session['s_user']
        print(request.session)
        print("=========================")
    return redirect('player:index')

otp = 0
forgot_password_email = ''

def forgotPassword(request):
    is_forgot_password = True
    is_received_email = False
    is_email_form = True
    headline1 = "Listen to Your Playlist again!!!"
    headline2 = "Forgot Password"
    validate_email = 0
    validate_otp = 0

    forms = FormForgotPassword()

    if request.POST.get('email'):
        print("Here============")
        email = request.POST.get('email')
        forms = FormForgotPassword(request.POST)
        # email = forms.cleaned_data['email']
        print(email)
        dict_user = Listener.objects.filter(email=email)
        print(dict_user)
        if dict_user.count() > 0:
            user = dict_user.values()[0]
            validate_email = '''
            <div class="alert alert-success" role="alert">
                OTP Code sent to your E-Mail account.
            </div>
            '''
            is_received_email = True
            numbers = string.digits
            globals()['otp'] = ''.join(choice(numbers) for _ in range(4))
            print(globals()['otp'])
            globals()['forgot_password_email'] = email
            
            #Send OTP mail
            subject = 'Sound Plan Recovery OTP Code'
            user_name = str(user['first_name']) + ' ' + str(user['last_name'])

            content = f'<p>Hi <b>{ user_name }</b>!,</p>'
            content += '<p>This is your Recovery code to your Forgot Password</p>'
            content += f'<h2>{ otp }</h2>'
            content += f'<p>Please ignore this E-Mail if this action is not Acknowledge by you.</p>'
            content += f'<p>Regards,</p>'
            content += f'<p>SoundPlan</p>'

            # send_mail(post.subject, content, EMAIL_HOST_USER, [post.email])
            msg = EmailMultiAlternatives(subject, content, EMAIL_HOST_USER, [email])
            msg.attach_alternative(content, 'text/html')
            msg.send()
            print("Successful Sent OTP mail")
            is_email_form = False
        else:
            validate_email = '''
            <div class="alert alert-danger" role="alert">
                E-Mail not Found!
            </div>
            '''

    if request.POST.get('otp'):
        user_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        print("Get OTP ", user_otp)
        print("Get new password ", new_password)
        print(globals()['otp'])
        user = Listener.objects.get(email=globals()['forgot_password_email'])
        print(user)
        if user_otp == globals()['otp']:
            change_password = hasher.encode(new_password, 'magic string')
            user.password = change_password
            user.save()
            validate_otp = '''
            <div class="alert alert-success" role="alert">
                Password change successfully!
            </div>
            '''
            return redirect('listener:login')
        else:
            is_received_email = True
            is_email_form = False
            validate_otp = '''
            <div class="alert alert-danger" role="alert">
                OTP Not Match!
            </div>
            '''

    return render(request, 'player/login.html', {
        'is_forgot_password' : is_forgot_password,
        'headline1' : headline1,
        'headline2' : headline2,
        'forms' : forms,
        'is_received_email' : is_received_email,
        'is_email_form' : is_email_form,
        'validate_email' : validate_email,
        'validate_otp' : validate_otp,
    })
