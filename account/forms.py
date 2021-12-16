import re
from bs4.element import ProcessingInstruction
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import requests
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'discord_webhook_url')

    def clean_discord(self):
        if self.cleaned_data['discord_webhook_url'] == None:
            return self.cleaned_data['discord_webhook_url']
        url = self.cleaned_data['discord_webhook_url']
        data = {"content": 'Congrats your webhook url is valid'}
        response = requests.post(url,json=data)
        if response.status_code != 204:
            raise ValidationError('Invalid webhook url')
        return url

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AccountManagementForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'discord_webhook_url']

    def clean_discord(self):
        if self.cleaned_data['discord_webhook_url'] == None:
            return self.cleaned_data['discord_webhook_url']
        url = self.cleaned_data['discord_webhook_url']
        data = {"content": 'Congrats your webhook url is valid'}
        response = requests.post(url,json=data)
        if response.status_code != 204:
            raise ValidationError('Invalid webhook url')
        return url