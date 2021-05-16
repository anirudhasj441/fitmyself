from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from home.models import Friend,UserExtended,ProfilePictures
from .models import Room, Message
import humanize
import json
import sys

# Create your views here.

def roomExists(user1,user2):
    rooms = Room.objects.filter(users = user1)
    name = False
    for room in rooms:
        if user2 in room.users.all():
            name = room.name
    return name
def messenger(request):
    if not request.user.is_authenticated:
        return redirect('/')
    room = Room.objects.filter(users = request.user).order_by("-updated").first()
    return redirect('/messenger/chat/'+str(room.name))
    
def createRoom(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    this_user = UserExtended.objects.get(user = request.user)
    chat_user = UserExtended.objects.get(slug = slug)
    user1 = request.user
    user2 = User.objects.get(pk = chat_user.user.pk)
    if not roomExists(request.user,user2):    
        name = "room"+this_user.slug+"."+chat_user.slug
        room = Room.objects.create(
            name = name,
        )
        room.users.add(user1)
        room.users.add(user2)
        room.save()
        return redirect('/messenger/chat/'+room.name)
    else:
        return redirect('/messenger/chat/'+str(roomExists(user1,user2)))

def chat(request,name):
    if not request.user.is_authenticated:
        return redirect('/')
    this_user = UserExtended.objects.get(user = request.user)
    rooms = Room.objects.filter(users=request.user).order_by("-updated")
    chat_room = Room.objects.get(name=name)
    users = chat_room.users.all()
    chats = Message.objects.filter(room = chat_room)
    show_chat = {}
    for user in users:
        if user == request.user:
            continue
        else:
            chat_user = user

    user_profile_pic = ProfilePictures.objects.filter(user=chat_user).order_by('-upload_on').first()
    friends = Friend.objects.filter(user= request.user)
    profile_pic = ProfilePictures.objects.filter(user=request.user).order_by('-upload_on').first()
    friends_profile_pics = {}
    room_user_profile_pic = {}
    for friend in friends:
        friends_profile_pics[friend] = ProfilePictures.objects.filter(user = friend.friends.user).order_by('-upload_on').first()

    for room in rooms:
        for user in room.users.all():
            if user.pk is not request.user.pk:
                room_user_profile_pic[user] = ProfilePictures.objects.filter(user = user).order_by("-upload_on").first()

    for room in rooms:
        show_chat[room] = Message.objects.filter(room = room).order_by('-time').first()

    demo_room = Room.objects.get(pk=7)
    demo_msg = Message.objects.filter(room = demo_room).order_by("-time").first()

    if request.method == "POST":
        try:
            msg = request.POST['message']
            attachment = request.FILES.get('attachment')
            message = Message.objects.create(
                user = request.user,
                room = chat_room,
                msg = msg,
                media = attachment,
            )
            chat_room.updated = timezone.now()
            chat_room.save()
        except:
            messages.error(request,sys.exc_info()[0])
            
    params = {
        'chat_friends' : friends,
        'friends_profile_pics' : friends_profile_pics,
        'media' : settings.MEDIA_URL,
        'chat_user' : chat_user,
        'user_profile_pic' : user_profile_pic,
        'room_user_profile_pic' : room_user_profile_pic,
        'profile_pic' : profile_pic,
        'chat_room' : chat_room,
        'rooms' : rooms,
        'chats' : chats,
        'show_chat' : show_chat,
        'this_user' : this_user,
    }
    return render(request,'messenger/index.html',params)

def getMessage(name):
    room = Room.objects.get(name = name)
    message = Message.objects.filter(room = room).order_by("-time").first()
    user = User.objects.filter(pk = message.user.pk).values('id','username','first_name','last_name')[0]
    data = {}
    data['user'] = user
    data['msg'] = message.msg
    data['media'] = str(message.media)
    data['time'] = message.time.strftime("%I:%M %p")
    data['seen'] = message.seen
    return data



# Signals

@receiver(post_save,sender=Message)
def send_message(sender,instance,created,*args,**kwargs):
    room = Room.objects.get(pk=instance.room.pk)
    channel_layer = get_channel_layer()
    data = getMessage(room.name)
    async_to_sync(channel_layer.group_send)(
        'message.'+str(room.name),{
            'type' : 'sendMessege',
            'values' : json.dumps(data)
        }
    )
