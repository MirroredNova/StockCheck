from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CreateUserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'discord')


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AccountManagementForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(AccountManagementForm, self).__init__(*args, **kwargs)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    discord = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'discord']


