from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    phone_regex = RegexValidator(regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
                                 message="Please enter a valid phone number")
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    discord_regex = RegexValidator(regex=r'^.{3,32}#[0-9]{4}$',
                                   message="Discord ID must be in the format string#1234")
    discord_webhook_url = models.CharField(max_length=400, blank=True, null=True)
