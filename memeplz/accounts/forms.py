from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    class Meta:
        model = Profile
        field = ['__all__',]
        exclude = ['user']