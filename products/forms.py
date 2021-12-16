from django import forms
from django.core.exceptions import ValidationError
from products.choices import *
from products.scrapers.best_buy_scraper import BestBuyScraper
from products.scrapers.amazon_scraper import amazon_scraper
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException
from requests.exceptions import MissingSchema


SUPPLIERS.insert(0, ('', '------'))
NOTIFICATION_INTERVAL.insert(0, ('', '------'))
NOTIFICATION_CHOICES.insert(0, ('', '------'))


class CreateDashboardBlockSupplier(forms.Form):
    supplier = forms.ChoiceField(choices=SUPPLIERS, required=True, label='Please Select a Supplier')


class CreateDashboardBlockAmazon(forms.Form):
    product_nickname = forms.CharField(max_length=400)
    # product_id = forms.CharField(max_length=20)
    NOTIFICATION_INTERVAL.insert(0, ('', '------'))
    NOTIFICATION_CHOICES.insert(0, ('', '------'))
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    product_url = forms.CharField(max_length=200)

    def clean_product_url(self):
        url = self.cleaned_data['product_url']
        if 'amazon' not in url:
            print('Invalid url ')
            raise ValidationError('Invalid URL')
        try:
            stock, price, name = amazon_scraper(url)
        except (MissingSchema, IndexError) as e:
            print('Invalid url ')
            raise ValidationError('Invalid URL')
        return url


class CreateDashboardBlockBestBuy(forms.Form):
    product_nickname = forms.CharField(max_length=400)
    # product_id = forms.CharField(max_length=20)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    product_url = forms.CharField(max_length=200)

    def clean_product_url(self):
        url = self.cleaned_data['product_url']
        best_buy_scraper = BestBuyScraper()
        try:
            stock, price, name = best_buy_scraper.get_price_bestbuy(url)
        except (InvalidArgumentException,NoSuchElementException) as e:
            print('Invalid url ')
            raise ValidationError('Invalid URL')
        return url


class CreateDashboardBlockCustom(forms.Form):
    product_nickname = forms.CharField(max_length=400)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    product_url = forms.CharField(max_length=200)
    product_xpath = forms.CharField(max_length=400)


class EditDashboardBlock(forms.Form):
    product_nickname = forms.CharField(max_length=200)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)


class EditDashboardBlockCustom(EditDashboardBlock):
    product_xpath = forms.CharField(max_length=400)