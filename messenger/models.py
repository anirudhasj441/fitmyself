from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def filePath(obj,filename):
    ext = filename.split('.')[-1]
    return "messenger/"+str(obj.user.first_name)+"."+str(obj.user.last_name)+"."+str(obj.user.pk)+"/"+str(obj.room.name)+"/media-"+str(obj.time)+"."+ext

class Room(models.Model):
    name = models.CharField(max_length = 1000)
    users = models.ManyToManyField(User)
    updated = models.DateTimeField(default=timezone.now)
    def user_list(self):
        return ",".join([str(user.first_name+" "+user.last_name) for user in self.users.all()])
    def __str__(self):
        return str(self.pk)

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    msg = models.CharField(max_length = 10000)
    media = models.FileField(upload_to=filePath,null=True,blank=True)
    time = models.DateTimeField(default = timezone.now)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return str(self.pk)

