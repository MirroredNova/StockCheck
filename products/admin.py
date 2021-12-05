from django.contrib import admin

# Register your models here.
from products.models import Product, UserProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'current_stock', 'current_price', 'last_updated', 'product_id', 'product_name', 'product_url']


class UserProductAdmin(admin.ModelAdmin):
    list_display = ['username', 'product', 'product_nickname', 'notification_interval', 'notification_method']


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
