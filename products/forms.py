from django import forms
from .models import Product, Supplier, UserProduct
from products.choices import *


class SupplierModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.supplier


class CreateDashboardBlockSupplier(forms.Form):
    supplier = SupplierModelChoiceField(queryset=Supplier.objects.all())


class CreateDashboardBlockAmazon(forms.Form):
    product_name = forms.CharField(max_length=400)
    product_id = forms.CharField(max_length=20)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
