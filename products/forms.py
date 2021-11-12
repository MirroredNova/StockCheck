from django import forms
from .models import Products


class CreateDashboardBlock(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('supplier', 'first_name', 'last_name', 'email', 'phone', 'discord')
