from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,login
from django.contrib import messages

# User defined Exceptions
class EmptyUserNameException(Exception):
    pass
class PasswordNotMatchException(Exception):
    pass
class EmptyPasswordException(Exception):
    pass
class WeakPasswordException(Exception):
    pass


# Create your views here.

def index(request):
    print(request.user.pk)
    return render(request,'home/index.html')

def signup(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            passwd = request.POST["password"]
            confirm_passwd = request.POST["con-password"]
            if len(passwd.replace(" ","")) == 0:
                raise EmptyPasswordException
            if passwd != confirm_passwd:
                raise PasswordNotMatchException
        except EmptyUserNameException:
            messages.error(request,"User Name Should Not Empty!")
        except EmptyPasswordException:
            messages.error(request,"Password Should Not Empty!")
        except PasswordNotMatchException:
            messages.error(request,"Password Not Matched!")
        else:
            user = User.objects.create_user(
                email,
                email,
                passwd,
                first_name=fname,
                last_name=lname
            )
            messages.success(request,"User created Successfully!")

    return render(request,'home/signup.html')

def signin(request):
    return render(request,'home/signin.html')


# APIs
def userLogut(request):
    logout(request)
    return redirect('/signin')