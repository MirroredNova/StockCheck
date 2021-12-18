from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
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
        if 'amazon' not in url and 'amzn' not in url:
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
    product_url = forms.CharField(max_length=200, label='Site URL')
    product_xpath = forms.CharField(max_length=400, label='Element XPath', help_text='The XPath pointing to the element indicating a product is out of stock, or that you want to see change.')
    product_element = forms.CharField(max_length=200, required=False, label='Element Contents', help_text='The HTML contents of the element the provided XPath points to.')


class EditDashboardBlock(forms.Form):
    product_nickname = forms.CharField(max_length=200)
    notification_interval = forms.ChoiceField(choices=NOTIFICATION_INTERVAL)
    notification_method = forms.ChoiceField(choices=NOTIFICATION_CHOICES)
    discord_url = forms.CharField(widget=forms.HiddenInput(),max_length=400,required=False,label="")

    def clean_discord_url(self):
        if self.cleaned_data['discord_url'] == '' and self.cleaned_data['notification_method'] == 'Discord':
            raise ValidationError("No webhook url on your account")
        return self.cleaned_data['discord_url']



class EditDashboardBlockCustom(EditDashboardBlock):
    product_xpath = forms.CharField(max_length=400, label='Element XPath',
                                    help_text='The XPath pointing to the element indicating a product is out of stock, or that you want to see change.')
    product_element = forms.CharField(max_length=200, required=False, label='Element Contents',
                                      help_text='The HTML contents of the element the provided XPath points to.')