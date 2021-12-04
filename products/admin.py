from django.contrib import admin

# Register your models here.
from products.models import Product, UserProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'current_stock', 'current_price', 'last_updated', 'product_id', 'product_object', 'product_nickname', 'product_url']


class UserProductAdmin(admin.ModelAdmin):
    list_display = ['username', 'product_object', 'notification_interval', 'notification_method']


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
