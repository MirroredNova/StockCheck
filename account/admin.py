from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


# Register your models here.
class User_admin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone', 'discord']


admin.site.register(User, User_admin)
