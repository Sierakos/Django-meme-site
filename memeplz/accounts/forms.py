from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django import forms
from .models import Profile

import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', 
                widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'invalid': 'Twój email jest nieprawidłowy'})
    password1 = forms.CharField(label='Hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label='Powtórz hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz Hasło'}))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].required = False

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            raise forms.ValidationError("ta nazwa użytkownika już istnieje. Wybierz inną")
        if not len(username) >= 5:
            raise forms.ValidationError("Nazwa użytkownika musi mieć conajmniej 5 znaków")
        if re.search('\s', username):
            raise forms.ValidationError("Nazwa użytkownika nie może zawierać spacji")
        if re.search("[!@#$%^&*(),.?\":{}|<>\\/;'[\]-\]]", username):
            raise forms.ValidationError("Nazwa użytkownika nie może zawierać znaków specjalnych oprócz _ (podłogi)")


        return username

    def clean_password1(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        if not re.search('[0-9]', password1):
            raise forms.ValidationError("Twoje hasło musi zawierać przynajmniej jedną cyfrę")
        if not len(password1) >= 8:
            raise forms.ValidationError("Twoje hasło musi mieć conajmniej 8 znaków")
        return password1

    def clean_password2(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Potwierdź swoje hasło")
        if password1 != password2:
            raise forms.ValidationError("Twoje hasła muszą być takie same")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login',
                            widget=forms.TextInput(attrs={'placeholder': 'Login'}),
                            required=False)
    password=forms.CharField(label='Hasło',
                            widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
                            required=False)

    class Meta:
        model = User
        fields = ['username']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # raise forms.ValidationError("Hasło lub login jest niepoprawne")
                pass

    

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='imię', max_length=120, required=False)
    last_name = forms.CharField(label='nazwisko', max_length=120, required=False)
    image = forms.ImageField(label='Zdjęcie profilowe', required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        field = ['__all__',]
        exclude = ['user']