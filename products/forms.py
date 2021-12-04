from django import forms
from products.choices import *

SUPPLIERS.insert(0, ('', '------'))
NOTIFICATION_INTERVAL.insert(0, ('', '------'))
NOTIFICATION_CHOICES.insert(0, ('', '------'))


class CreateDashboardBlockSupplier(forms.Form):
    supplier = forms.ChoiceField(choices=SUPPLIERS, required=True, label='Please Select a Supplier')


class CreateDashboardBlockAmazon(forms.Form):
    product_nickname = forms.CharField(max_length=200)
    product_id = forms.CharField(max_length=20)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    product_url = forms.CharField(max_length=200)


class EditDashboardBlock(forms.Form):
    product_nickname = forms.CharField(max_length=200)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
