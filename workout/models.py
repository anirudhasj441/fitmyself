from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Workout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    parts = models.CharField(max_length=50,null=True)
    slug = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.pk)

class Exercise(models.Model):
    workout = models.ForeignKey(Workout,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    repetition = models.CharField(max_length=50)
    sets = models.IntegerField(null=True)
    def __str__(self):
        return str(self.pk)