from django.contrib import admin

# Register your models here.
from products.models import Product, UserProduct, Supplier


class ProductAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'current_stock', 'current_price', 'last_updated', 'product_id', 'product_name']


class UserProductAdmin(admin.ModelAdmin):
    list_display = ['username', 'product_name', 'notification_interval', 'notification_method']


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier']


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
