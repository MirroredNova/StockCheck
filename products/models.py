from bs4.builder import TreeBuilder
from django.db import models
from account.models import User
from products.choices import *


class Product(models.Model):
    product_id = models.CharField(max_length=30)
    product_name = models.CharField(max_length=200)
    product_url = models.CharField(max_length=200)
    supplier = models.CharField(max_length=20,
                                choices=SUPPLIERS)
    current_stock = models.BooleanField()
    current_price = models.DecimalField(decimal_places=2, max_digits=20)
    last_updated = models.DateTimeField()
    product_object = models.CharField(max_length=200)


class UserProduct(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_nickname = models.CharField(max_length=200, default='Nickname')
    notification_interval = models.CharField(max_length=200,
                                             choices=NOTIFICATION_INTERVAL,
                                             default=MED)
    notification_method = models.CharField(max_length=200,
                                           choices=NOTIFICATION_CHOICES,
                                           default=EMAIL)

