from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from home.models import Friend,UserExtended

# Create your views here.

def messenger(request):
    if not request.user.is_authenticated:
        return redirect('/')
    friends = Friend.objects.filter(user= request.user)

    params = {
        'chat_friends' : friends,
    }
    
    return render(request,'messenger/index.html',params)

def chat(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request,'messenger/index.html')