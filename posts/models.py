from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def imgPath(obj,filename):
    ext = filename.split('.')[-1]
    return "uploads/"+str(obj.user.first_name)+"."+obj.user.last_name+"."+str(obj.user.pk)+"uploads/post-"+str(obj.upload_on)+"."+ext

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    desc = models.TextField(null=True,blank=True)
    media = models.FileField(upload_to=imgPath,null=True,blank=True)
    upload_on = models.DateTimeField(default= timezone.now)
    slug = models.TextField(null=True,blank=True)
    def fileType(self):
        ext = self.media.name.split('.')[-1]
        if ext == "jpeg" or ext == "jpg" or ext == "svg" or ext == "ico":
            return "image"
        elif ext == "mp4" or ext == "webm" or ext == "ogg" or ext == "mkv":
            return "video"
        else:
            return "not-defined"
    def __str__(self):
        return str(self.pk)

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.pk)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length = 100,null=True,blank=True)
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.pk)