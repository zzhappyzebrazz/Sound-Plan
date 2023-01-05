
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


    # Change password
    if 's_user' not in request.session:
        print('User unregisterd')
        return redirect('player:index')
    
    # Show user infomation CHECK
    user = request.session['s_user']
    print(user)

    info_forms = FormUpdateInfo(initial={
        'first_name' : user['first_name'],
        'last_name' : user['last_name'],
        'phone' : user['phone'],
        'address' : user['address'],
    })
            
    # Update user infomation
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
            
            #Update to sesstion
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
                    Plase Fill out the Form!!!
                </div>
            '''
    
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
                        Plase Fill out the Form!!!
                    </div>
                '''
    return render(request, 'player/my-account.html', {
        'user' : user,
        'info_forms' : info_forms,
        'password_forms' : password_forms,
        'result_update_info' : result_update_info,
        'result_change_password' : result_change_password,
    })

def logout(request):
    if 's_user' in request.session:
        del request.session['s_user']
        print(request.session)
        print("=========================")
    return redirect('player:index')