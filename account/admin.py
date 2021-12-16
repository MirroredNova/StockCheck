from django.contrib import admin

from account.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone', 'discord_webhook_url']


admin.site.register(User, UserAdmin)
