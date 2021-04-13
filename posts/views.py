from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Post,Comment
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


#APIs
def comment(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    post = Post.objects.get(slug = slug)
    if request.method == "POST":
        comment = request.POST['comment']
        comm = Comment.objects.create(
            post = post,
            user = request.user,
            comment = comment,
        )
    return redirect('/')