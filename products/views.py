from django.shortcuts import render, redirect
import datetime
from products.forms import CreateDashboardBlockSupplier, CreateDashboardBlockAmazon
from core.models import Products, UserProducts


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
            product = Products()
            user_prod = UserProducts()

            now = datetime.datetime.now()
            #current_time = now.strftime("%H:%M:%S")

            product.supplier = supplier
            product.current_stock = False  # should be initialized to the initial check result
            product.current_price = 0  # should be initialized to the initial check result
            product.last_updated = now
            product.product_id = form.cleaned_data['product_id']
            #print(f'Product id is {product.product_id}')
            product.product_name = form.cleaned_data['product_name']
            product.product_url = form.cleaned_data['product_url']
            product.save()

            user_prod.username = request.user
            user_prod.product_object = product
            if form.cleaned_data['notification_interval'] == 'Fast':
                user_prod.notification_interval = '1_min'
            elif form.cleaned_data['notification_interval'] == 'Medium':
                user_prod.notification_interval = '10_min'
            elif form.cleaned_data['notification_interval'] == "Slow":
                user_prod.notification_interval = '1_hour'
            else:
                print(form.cleaned_data['notification_interval'])
            
            #user_prod.notification_interval = form.cleaned_data['notification_interval']
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
