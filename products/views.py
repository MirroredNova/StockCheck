from django.shortcuts import render, redirect
import datetime
from products import choices
from products.forms import *
from products.models import Product, UserProduct
from products.scrapers import amazon_scraper, best_buy_scraper
from products.scrapers.custom_site_scraper import custom_site_scraper


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
        if supplier == choices.AMAZON:
            form = CreateDashboardBlockAmazon(request.POST)
        elif supplier == choices.BEST_BUY:
            form = CreateDashboardBlockBestBuy(request.POST)
        elif supplier == choices.CUSTOM:
            form = CreateDashboardBlockCustom(request.POST)
        else:
            pass

        if form.is_valid():
            product = Product()
            user_prod = UserProduct()

            now = datetime.datetime.now()

            url = form.cleaned_data['product_url']

            if supplier == choices.AMAZON:
                stock, price, name = amazon_scraper.amazon_scraper(url)
            elif supplier == choices.BEST_BUY:
                scraper = best_buy_scraper.BestBuyScraper()
                stock, price, name = scraper.get_price_bestbuy(url)
            elif supplier == choices.CUSTOM:
                xpath = form.cleaned_data['product_xpath']
                product.product_xpath = xpath
                name, price = 'custom', 0
                stock = custom_site_scraper(url, xpath, '')
            else:
                return redirect('/choose_supplier/')

            product.supplier = supplier
            product.current_stock = stock  # should be initialized to the initial check result
            product.current_price = price  # should be initialized to the initial check result
            product.last_updated = now
            product.product_name = name
            # product.product_id = form.cleaned_data['product_id']
            product.product_url = url

            product.save()

            user_prod.username = request.user

            user_prod.product = product
            user_prod.product_nickname = form.cleaned_data['product_nickname']
            # this saves the constant value in 'choices.py' by default, no conversions necessary
            user_prod.notification_interval = form.cleaned_data['notification_interval']
            user_prod.notification_method = form.cleaned_data['notification_method']
            user_prod.save()

            return redirect('/dashboard/')
    else:
        print(supplier)
        if supplier == choices.AMAZON:
            form = CreateDashboardBlockAmazon()
        elif supplier == choices.BEST_BUY:
            form = CreateDashboardBlockBestBuy()
        elif supplier == choices.CUSTOM:
            form = CreateDashboardBlockCustom()
        else:
            pass
    return render(request, 'choose_product.html', {
        'form': form,
    })


def edit_product(request, data):
    user_prod = UserProduct.objects.filter(id=data).first()
    product = user_prod.product
    discord_url = user_prod.username.discord_webhook_url

    initial_vals = {'product_nickname': user_prod.product_nickname,
                    'notification_interval': user_prod.notification_interval,
                    'notification_method': user_prod.notification_method, 
                    'discord_url': discord_url,}

    if request.method == 'POST':
        if product.supplier == choices.CUSTOM:
            initial_vals['product_xpath'] = product.product_xpath
            form = EditDashboardBlockCustom(request.POST, initial=initial_vals)
        else:
            form = EditDashboardBlock(request.POST, initial=initial_vals)
        if form.is_valid():
            user_prod.product_nickname = form.cleaned_data['product_nickname']
            user_prod.notification_interval = form.cleaned_data['notification_interval']
            user_prod.notification_method = form.cleaned_data['notification_method']
            if product.supplier == choices.CUSTOM:
                product.product_xpath = form.cleaned_data['product_xpath']
                product.save()
            user_prod.save()
    else:
        if product.supplier == choices.CUSTOM:
            initial_vals['product_xpath'] = product.product_xpath
            form = EditDashboardBlockCustom(initial=initial_vals)
        else:
            form = EditDashboardBlock(initial=initial_vals)
    return render(request, 'edit_product.html', {
        'name': user_prod.product_nickname,
        'form': form,
    })


def delete_user_product(request, data):
    UserProduct.objects.filter(id=data).delete()
    product = UserProduct.objects.filter(username=request.user)
    return render(request, 'dashboard.html', {'UserProduct': product})
