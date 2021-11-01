from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField


class CreateUserForm(UserCreationForm):

    class Meta(UserCreationForm):
        phone = PhoneNumberField()
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'discord')


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
