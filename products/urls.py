from django.urls import path
import products.views

urlpatterns = [
    # paths for general account authentication and management
    path('choose_supplier/', products.views.choose_supplier, name="choose_supplier"),
    path('choose_product/', products.views.choose_product, name="choose_product"),
    path('edit_product/<str:data>', products.views.edit_product, name="edit_product"),
]
