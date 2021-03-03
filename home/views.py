from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.db import IntegrityError
from .models import UserExtended
import re
import sys

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

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        messages.info(request,"Please Login to explore content")
        return redirect('/signin')
    return render(request,'home/index.html')

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
                UserExtended.objects.create(
                    user = user,
                    dob = dob,
                    gender = gender,
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


# APIs
def userLogut(request):
    logout(request)
    return redirect('/signin')