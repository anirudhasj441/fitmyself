from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from posts.models import Post,Comment,Like
from .models import UserExtended,ProfilePictures,CoverPicture,FriendRequest,Friend,Notification
from datetime import datetime
from django.http import JsonResponse
import json
import re
import sys
import os

# User defined Exceptions
class EmptyUserNameException(Exception):
    pass
class PasswordNotMatchException(Exception):
    pass
class EmptyPasswordException(Exception):
    pass
class WeakPasswordException(Exception):
    pass


# custom functions
def checkPassword(password):
    if (len(password)<8): 
        return False
    elif not re.search("[a-z]", password): 
        return False
    elif not re.search("[A-Z]", password): 
        return False
    elif not re.search("[0-9]", password): 
        return False
    elif not re.search("[_@$]", password): 
        return False
    elif re.search("\s", password): 
        return False
    else:
        return True

def deleteFilePath(path):
    print(path)
    if os.path.isfile(path):
        print(True)
        os.remove(path)
    else:
        print(False)

def isLiked(post,user):
    likes = Like.objects.filter(post=post)
    liked_users = []
    for like in likes:
        liked_users.append(like.user)
    if user in liked_users:
        return True
    else:
        return False

def isFriend(user1,user2):
    friend = Friend.objects.filter(user = user1,friends = user2)
    if friend:
        return True
    else:
        return False

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        messages.info(request,"Please Login to explore content")
        return redirect('/signin')
    page = request.GET.get('page',1)
    profile_pictures = {}
    friend_picture = {}
    likes = {}
    liked = {}
    posts = []
    comments = {}
    comment_profile_pic = {}
    friend_user = []
    friends = Friend.objects.filter(user = request.user)
    posts.append(Post.objects.filter(user=request.user).order_by("-upload_on"))
    for friend in friends:
        # posts.append(Post.objects.filter(user=user.friends.user).order_by("-upload_on"))
        friend_user.append(friend.friends.user)

    post_list = Post.objects.filter(Q(user__in=friend_user) | Q(user = request.user)).order_by("-upload_on")
    for post in post_list:
        profile_pictures[post] = ProfilePictures.objects.filter(user=post.user).order_by("-upload_on").first()
        likes[post] = Like.objects.filter(post=post).order_by("-time")
        liked[post] = isLiked(post,request.user)
        comments[post] = Comment.objects.filter(post = post).order_by("time")
        for comment in comments[post]:
            comment_profile_pic[comment] = ProfilePictures.objects.filter(user = comment.user).order_by("-upload_on").first()
    for friend in friends:
        friend_picture[friend] = ProfilePictures.objects.filter(user = friend.friends.user).order_by("-upload_on").first()
    
    paginator = Paginator(post_list,3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    params = {
        'posts' : posts,
        'post_profile_pictures' : profile_pictures,
        'likes' : likes,
        'liked' : liked,
        'friends' : friends,
        'friend_picture' : friend_picture,
        'comments' : comments,
        'comment_profile_pic' : comment_profile_pic,
        'media' : settings.MEDIA_URL,
    }
    return render(request,'home/index.html',params)

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                email = request.POST["email"]
                fname = request.POST["fname"]
                lname = request.POST["lname"]
                passwd = request.POST["password"]
                confirm_passwd = request.POST["con-password"]
                dob = request.POST["dob"]
                gender = request.POST["gender"]
                if passwd != confirm_passwd:
                    raise PasswordNotMatchException
                if len(email.replace(" ","")) == 0:
                    raise EmptyUserNameException
                if len(passwd.replace(" ","")) == 0:
                    raise EmptyPasswordException
                if not checkPassword(passwd):
                    raise WeakPasswordException
                user_created = False
                user = User.objects.create_user(
                    email,
                    email,
                    passwd,
                    first_name=fname,
                    last_name=lname
                )
                user_created = True
                slug = user.first_name+"."+user.last_name+"."+str(user.pk)
                print(slug)
                UserExtended.objects.create(
                    user = user,
                    dob = dob,
                    gender = gender,
                    slug = slug,
                )
            except EmptyUserNameException:
                messages.error(request,"User Name Should Not Empty!")
            except EmptyPasswordException:
                messages.error(request,"Password Should Not Empty!")
            except PasswordNotMatchException:
                messages.error(request,"Password Not Matched!")
            except WeakPasswordException:
                messages.warning(request,"A good password must be follow below condition:\n1.It\'s Length Should not be less than 8.\n2.It is combination of one number, one Capital letter, one small letter and one special character")
            except IntegrityError:
                messages.warning(request,"Its seems that you have alredy have an Account Please log In.")
            except:
                if user_created:
                    user.delete()
                messages.error(request,sys.exc_info()[0])
            else:
                messages.success(request,"User created Successfully!")
    else:
        return redirect("/")

    return render(request,'home/signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST["email"]
        passwd = request.POST["password"]
        user = authenticate(
            username = email,
            password = passwd
        )
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'home/signin.html')

def userProfilePage(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    this_user = UserExtended.objects.get(slug = slug)
    posts = Post.objects.filter(user=this_user.user).order_by("-upload_on")
    cover_pic = CoverPicture.objects.filter(user=this_user.user).order_by("-upload_on").first()
    profile_pic = ProfilePictures.objects.filter(user = this_user.user).order_by("-upload_on").first()
    user = UserExtended.objects.get(user=request.user)
    friend_request = FriendRequest.objects.filter(user=this_user.user,sent_by=user).first()
    has_request = FriendRequest.objects.filter(user=request.user,sent_by=this_user).first()
    friends = Friend.objects.filter(user = this_user.user)
    friend_pictures = {}
    photos = []
    profile_pictures = {}
    likes = {}
    liked = {}
    profile_pics = ProfilePictures.objects.filter(user = this_user.user).order_by("-upload_on")
    cover_pics = CoverPicture.objects.filter(user=this_user.user).order_by("-upload_on")
    for pic in profile_pics:
        photos.append(pic.display_picture)
    for pic in cover_pics:
        photos.append(pic.cover_photo)
        
    for post in posts:
        profile_pictures[post] = ProfilePictures.objects.filter(user=post.user).order_by("-upload_on").first()
        likes[post] = Like.objects.filter(post=post)
        liked[post] = isLiked(post,request.user)

    for friend in friends:
        friend_pictures[friend] = ProfilePictures.objects.filter(user = friend.friends.user).order_by("-upload_on").first()
    params = {
        'this_user' : this_user,
        'cover_pic' : cover_pic,
        'posts' : posts,
        'profile_pic' : profile_pic,
        'post_profile_pictures' : profile_pictures,
        'likes' : likes,
        'liked' : liked,
        'photos' : photos,
        'friend_request' : friend_request,
        'has_request' : has_request,
        'is_friend' : isFriend(request.user,this_user),
        'friends' : friends,
        'friend_picture' : friend_pictures,
        'media' : settings.MEDIA_URL,
    }
    return render(request,'home/profile.html',params)

def userPhotos(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    this_user = UserExtended.objects.get(slug=slug)
    cover_pics = CoverPicture.objects.filter(user=this_user.user).order_by("-upload_on")
    profile_pics = ProfilePictures.objects.filter(user = this_user.user).order_by("-upload_on")
    params = {
        'this_user' : this_user,
        'cover_pics' : cover_pics,
        'profile_pics' : profile_pics,
        'cover_pic' : cover_pics.first(),
        'profile_pic' : profile_pics.first(),
        'media' : settings.MEDIA_URL,
    }
    return render(request,'home/photos.html',params)

def userFriends(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    this_user = UserExtended.objects.get(slug = slug)
    profile_pic = ProfilePictures.objects.filter(user = this_user.user).order_by("-upload_on").first()
    cover_pic = CoverPicture.objects.filter(user = this_user.user).order_by("-upload_on").first()
    friends = Friend.objects.filter(user = this_user.user)
    friend_profile_pic = {}
    for friend in friends:
        friend_profile_pic[friend] = ProfilePictures.objects.filter(user = friend.friends.user).order_by("-upload_on").first()
    params = {
        'this_user' : this_user,
        'profile_pic' : profile_pic,
        'cover_pic' : cover_pic,
        'friends' : friends,
        'friend_profile_pic' : friend_profile_pic,
        'media' : settings.MEDIA_URL,
    }
    return render(request,'home/friends.html',params)


# APIs
def userLogut(request):
    logout(request)
    return redirect('/signin')
    
def uploadProfilePic(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    user = UserExtended.objects.get(slug = slug)
    if user == UserExtended.objects.get(user = request.user):
        if request.method == "POST" and request.FILES:
            pic = request.FILES["pic"]
            if pic is not None:
                profile_pic = ProfilePictures.objects.create(
                    user = request.user,
                    display_picture = pic,
                )
                
        return redirect('/user/'+str(user.slug))
    else:
        return redirect('/')

def uploadCoverPic(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    user = UserExtended.objects.get(slug = slug)
    if not user == UserExtended.objects.get(user = request.user):
        return redirect('/')
    if request.method == "POST":
        pic = request.FILES['pic']
        if pic is not None:
            cover_pic = CoverPicture.objects.create(
                user = request.user,
                cover_photo = pic,
            )
            
    return redirect('/user/'+str(user.slug))

def likePost(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    post = Post.objects.get(slug = slug)
    Like.objects.create(
        user = request.user,
        post = post,
    )
    return redirect('/')

def unlikePost(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    post = Post.objects.get(slug=slug)
    like = Like.objects.get(post=post,user=request.user).delete()
    return redirect('/')

def sendFriendRequest(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    send_to = UserExtended.objects.get(slug=slug)
    sent_by = UserExtended.objects.get(user = request.user)
    slug = "request."+request.user.first_name+"."+request.user.last_name+".-"+send_to.user.first_name+"."+send_to.user.last_name+"."+str(datetime.now())
    friend_request = FriendRequest.objects.create(
        user = send_to.user,
        sent_by = sent_by,
        slug = slug,
    )
    return redirect('/user/'+str(send_to.slug))

def cancelRequest(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    friend_request = FriendRequest.objects.get(slug=slug)
    user = UserExtended.objects.get(user = friend_request.user)
    friend_request.delete()
    return redirect('/user/'+user.slug)

def deleteRequest(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    friend_request = FriendRequest.objects.get(slug=slug)
    user = friend_request.sent_by
    friend_request.delete()
    return redirect('/user/'+str(user.slug))

def acceptRequest(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    friend_request = FriendRequest.objects.get(slug = slug)
    sent_to = friend_request.user
    sent_by = friend_request.sent_by
    friend_request.accepted = True
    friend_request.save()
    user = UserExtended.objects.get(user = sent_to)
    friend = Friend.objects.create(
        user = sent_to,
        friends = sent_by,
    )
    friend = Friend.objects.create(
        user = sent_by.user,
        friends = user,
    )
    return redirect('/user/'+str(sent_by.slug))

def notificationSeen(request,slug):
    notification = Notification.objects.get(slug = slug)
    notification.seen = True
    notification.save()
    if notification.notification_type == "post":
        return redirect('/')
    elif notification.notification_type == "friend request":
        return redirect('/user/'+str(notification.friend_request.sent_by.slug))

        
# Signals(Triggers)

@receiver(post_save,sender=ProfilePictures)
def addProfilePic(sender,instance,*args,**kwargs):
    post = Post.objects.create(
        user =  instance.user,
        desc = instance.user.first_name +" "+instance.user.last_name+" change profile picture",
        media = instance.display_picture,
        slug = "post"+str(instance.user.first_name)+"."+str(instance.user.last_name)+"."+str(datetime.now()),
    )

@receiver(post_save,sender=CoverPicture)
def addCoverPic(sender,instance,*args,**kwargs):
    post = Post.objects.create(
        user = instance.user,
        desc = instance.user.first_name +" "+instance.user.last_name + " change cover pic",
        media = instance.cover_photo,
        slug = "post"+str(instance.user.first_name)+"."+str(instance.user.last_name)+"."+str(datetime.now()),
    )

@receiver(post_save,sender=Post)
def addNotificationForPost(sender,instance,created,*args,**kwargs):
    if created:
        nottification = Notification.objects.create(
            user = instance.user,
            time = instance.upload_on,
            notification_type = 'post',
            post = instance,
            slug = "notification-post-"+str(instance.pk)
        )

@receiver(post_save,sender=FriendRequest)
def addNotificationForFriendRequest(sender,instance,created,*args,**kwargs):
    if created:
        notification = Notification.objects.create(
            user = instance.user,
            time = instance.time,
            notification_type = 'friend request',
            friend_request = instance,
            slug = 'notification-friend-request-'+str(instance.pk)
        )

@receiver(pre_delete,sender=ProfilePictures)
def deleteImage(sender,instance,*args,**kwargs):
    profile_picture = ProfilePictures.objects.get(pk=instance.pk)
    deleteFilePath(str(profile_picture.display_picture.path))

# @receiver(pre_delete,sender=FriendRequest)
# def deleteNotificationForRequest(sender,instance,*args,**kwargs):
#     notification_for_friend_request = NotificationsForFriendRequest.objects.get(
#         friend_request = instance
#     ).delete()
#     nottification = Notification.objects.get(slug = "notification-friend-request-"+str(instance.pk)).delete()