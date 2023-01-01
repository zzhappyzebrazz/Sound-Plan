from django import forms
from listener.models import Listener


class FormRegister(forms.ModelForm):
    first_name = forms.CharField(max_length=264, label='First name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "First name",
    }))
    last_name = forms.CharField(max_length=264, label='Last name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Last name",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Password",
    }))
    confirm_password = forms.CharField(label='Confirmed password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Confirmed password",
    }))
    phone = forms.CharField(max_length=20, label='Phone number', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Phone number",
    }))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Address", "rows": "3",
    }))

    class Meta:
        model = Listener
        fields = '__all__'


