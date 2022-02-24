from django.db import models
from django.conf import settings
from django.utils import timezone 

# Create your models here.

class Clock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField(null=True, blank=True)
    
class ClockedHours(models.Model):
    today = models.IntegerField()
    current_week = models.IntegerField()
    current_month = models.IntegerField()
    

    