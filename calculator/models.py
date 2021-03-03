from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Bmr(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  bmr = models.CharField(max_length=30,null=True)
  date_filled = models.DateTimeField(default=timezone.now)

class Bmi(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  bmi = models.CharField(max_length=30,null=True)
  date_filled = models.DateTimeField(default=timezone.now)