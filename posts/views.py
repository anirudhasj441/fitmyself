from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Post
from datetime import datetime
import sys

# Create your views here.


def addPost(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        # try:
            desc = request.POST.get('desc')
            post_media = request.FILES.get('post-media')
            slug = "post"+str(request.user.first_name)+"."+str(request.user.last_name)+"."+str(datetime.now())
            post = Post.objects.create(
                user = request.user,
                desc = desc,
                media = post_media,
                slug = slug,
            )
        # except Exception:
            messages.error(request,sys.exc_info()[0])
    return redirect('/')