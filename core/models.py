from django.db import models
from account.models import User

# Create your models here.

class Products(models.Model):
    supplier = models.CharField(max_length=200)
    current_stock = models.BooleanField()
    current_price = models.DecimalField(decimal_places=2,max_digits=20)
    last_updated = models.TimeField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)


class UserProducts(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    product_name = models.OneToOneField(Products,on_delete=models.CASCADE)
    notification_interval = models.CharField(max_length=200)
    notification_method = models.CharField(max_length=200)

class NotificationQueue(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_method = models.CharField(max_length=200)
