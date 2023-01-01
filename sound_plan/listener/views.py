
from django.shortcuts import render, redirect
from listener.forms import FormRegister
from listener.models import Listener
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Create your views here.
def login(request):
    print('###LOGIN###')
    return render(request, 'player/login.html')

def register(request):
    print('###REGISTER###')
    #THỰC HIỆN CHỨC NĂNG ĐĂNG KÝ
    forms = ''
    hasher = PBKDF2PasswordHasher()
    result_register = ''
    is_ok = False
    if request.POST.get('first_name'):
        forms = FormRegister(request.POST, Listener)
        if forms.is_valid():
            print('Get valid POST from LISTENER')
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

                result_register = '''
                        <div class="alert alert-success" role="alert">
                            Registersuccess!
                        </div>
                        '''
                is_ok = True
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


    if is_ok:
        return redirect('listener:login')
    
    return render(request, 'player/register.html', {
        'forms' : forms,
        'result_register' : result_register,
        
    })