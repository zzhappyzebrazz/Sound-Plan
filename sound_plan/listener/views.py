
from django.shortcuts import render, redirect
from listener.forms import *
from listener.models import Listener
from sound_plan.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.hashers import PBKDF2PasswordHasher

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
    #TO-DO:
    # Show user infomation
    # Update user infomation
    # Change password
    
    if 's_user' in request.session:
        user = request.session['s_user']
        print(user)
        info_forms = FormRegister(initial={
            'first_name' : user['first_name'],
            'last_name' : user['last_name'],
            'email' : user['email'],
            'phone' : user['phone'],
            'address' : user['address'],
        })
        
        info_forms.fields['email'].widget.attrs['readonly'] = True
        
        password_forms = FormUserChangePassword()
        return render(request, 'player/my-account.html', {
            'user' : user,
            'info_forms' : info_forms,
            'password_forms' : password_forms,
        })
    else:
        print('User unregisterd')
        return redirect('player:index')

def logout(request):
    if 's_user' in request.session:
        del request.session['s_user']
        print(request.session)
        print("=========================")
    return redirect('player:index')