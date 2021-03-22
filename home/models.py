from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def dpPath(obj,filename):
    ext = filename.split('.')[-1]
    return "uploads/"+str(obj.user.first_name)+"."+obj.user.last_name+"."+str(obj.user.pk)+"/display_picture/display_picture-"+str(obj.upload_on)+"."+ext

def coverPhotoPath(obj,filename):
    ext = filename.split('.')[-1]
    return "uploads/"+str(obj.user.first_name)+"."+str(obj.user.last_name)+"."+str(obj.user.pk)+"/cover_photo/cover_photo-"+str(obj.upload_on)+"."+ext

class ProfilePictures(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    upload_on = models.DateTimeField(default = timezone.now,null=True)
    display_picture = models.ImageField(upload_to=dpPath,null=True,blank=True)
    def __str__(self):
        return str(self.pk)

class CoverPicture(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    upload_on = models.DateTimeField(default = timezone.now,null = True,blank=True)
    cover_photo = models.ImageField(upload_to = coverPhotoPath,null=True,blank=True)
    def __str__(self):
        return str(self.pk)

class UserExtended(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=50,null=True)
    slug = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.user.first_name)+" "+str(self.user.last_name)

class Friend(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    friends = models.ForeignKey(UserExtended,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)

class FriendRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sent_by = models.ForeignKey(UserExtended,on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)
    slug = models.TextField(max_length=500)
    def __str__(self):
        return str(self.user.first_name)