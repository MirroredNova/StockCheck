from django.db import models
from account.models import User


# Create your models here.
class NotificationQueue(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_method = models.CharField(max_length=200)
    message = models.CharField(max_length=400,default='lol')
    discord_url = models.CharField(max_length=400,blank=True,null=True)
