from django import forms
from products.choices import *


class CreateDashboardBlockSupplier(forms.Form):
    SUPPLIERS.insert(0, ('', '------'))
    supplier = forms.ChoiceField(choices=SUPPLIERS, required=True, label='Please Select a Supplier')


class CreateDashboardBlockAmazon(forms.Form):
    product_name = forms.CharField(max_length=400)
    product_id = forms.CharField(max_length=20)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    product_url = forms.CharField(max_length=200)
