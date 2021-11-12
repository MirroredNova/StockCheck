from django.db import models
from account.models import User


# Create your models here.
class NotificationQueue(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_method = models.CharField(max_length=200)
