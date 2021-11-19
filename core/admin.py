from django.contrib import admin
from .models import Products, UserProducts, NotificationQueue

# Register your models here.
admin.site.register(Products)
admin.site.register(UserProducts)
admin.site.register(NotificationQueue)