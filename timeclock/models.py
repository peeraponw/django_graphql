from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import DateTimeField

# Create your models here.
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Clock(models.Model):
    user = models.ForeignKey(ExtendUser, on_delete=models.DO_NOTHING)
    clocked_in = models.DateTimeField()
    clocked_out = models.DateTimeField()
    
class ClockedHours(models.Model):
    today = models.IntegerField()
    current_week = models.IntegerField()
    current_month = models.IntegerField()
    

    