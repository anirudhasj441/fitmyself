from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def dpPath(obj,filename):
        return "uploads/User_"+obj.user.pk+"/display_picture/"+filename


class UserExtended(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    display_picture = models.ImageField(upload_to=dpPath,null=True,blank=True)


class Workout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    parts = models.CharField(max_length=50,null=True)
    def __str__(self):
        return str(self.pk)

class Exercie(models.Model):
    workout = models.ForeignKey(Workout,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    repetition = models.CharField(max_length=50)
    sets = models.IntegerField(null=True)
    def __str__(self):
        return str(self.pk)