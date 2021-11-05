from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    phone = PhoneNumberField(blank=False)
    discord_regex = RegexValidator(regex=r'^.{3,32}#[0-9]{4}$',
                                   message="Discord ID must be in the format string#1234")
    discord = models.CharField(validators=[discord_regex], max_length=40, blank=False)
