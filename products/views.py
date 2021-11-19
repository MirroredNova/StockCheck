from django.shortcuts import render, redirect
import datetime
from products.forms import CreateDashboardBlockSupplier, CreateDashboardBlockAmazon
from products.models import Product, UserProduct


def choose_supplier(request):
    if request.method == 'POST':
        form = CreateDashboardBlockSupplier(request.POST)
        if form.is_valid():
            supplier = form.cleaned_data['supplier']
            request.session['chosen_supplier'] = supplier
            return redirect('/choose_product/')
    else:
        form = CreateDashboardBlockSupplier()
    return render(request, 'choose_supplier.html', {
        'form': form,
    })


def choose_product(request):
    supplier = request.session['chosen_supplier']
    if request.method == 'POST':
        if supplier == 'Amazon':
            form = CreateDashboardBlockAmazon(request.POST)
        else:
            pass

        if form.is_valid():
            product = Product()
            user_prod = UserProduct()

            now = datetime.datetime.now()

            product.supplier = supplier
            product.current_stock = False  # should be initialized to the initial check result
            product.current_price = 0  # should be initialized to the initial check result
            product.last_updated = now
            product.product_id = form.cleaned_data['product_id']
            product.product_name = form.cleaned_data['product_name']
            product.product_url = form.cleaned_data['product_url']
            product.save()

            user_prod.username = request.user
            user_prod.product_name = product
            # this saves the constant value in 'choices.py' by default, no conversions necessary
            user_prod.notification_interval = form.cleaned_data['notification_interval']
            user_prod.notification_method = form.cleaned_data['notification_method']
            user_prod.save()

            return redirect('/dashboard/')
    else:
        print(supplier)
        if supplier == 'Amazon':
            form = CreateDashboardBlockAmazon()
        else:
            pass
    return render(request, 'choose_supplier.html', {
        'form': form,
    })
