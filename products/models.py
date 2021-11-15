from django.db import models
from account.models import User
from products.choices import *


class Supplier(models.Model):
    supplier = models.CharField(max_length=200, primary_key=True)


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    current_stock = models.BooleanField()
    current_price = models.DecimalField(decimal_places=2, max_digits=20)
    last_updated = models.TimeField()
    product_id = models.CharField(max_length=30)
    product_name = models.CharField(max_length=200)


class UserProduct(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    notification_interval = models.CharField(max_length=200,
                                             choices=NOTIFICATION_INTERVAL,
                                             default=MED)
    notification_method = models.CharField(max_length=200,
                                           choices=NOTIFICATION_CHOICES,
                                           default=EMAIL)

