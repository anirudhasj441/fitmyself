from django.shortcuts import render,redirect
from .models import Bmi,Bmr
from home.models import UserExtended
from django.contrib import messages
from datetime import date
import sys

def ageCalculate(birthDate):
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age

# Create your views here.

def bmrCalculator(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = UserExtended.objects.get(user=request.user)
    if request.method == "POST":
        try:
            bmr = request.POST['bmr']
            Bmr.objects.filter(user=request.user).delete()
            Bmr.objects.create(
                user = request.user,
                bmr = bmr
            )
        except:
            messages.error(request,sys.exc_info()[0])
        
    params = {
        'user' : user,
        'dob' : ageCalculate(user.dob),
    }
    
    return render(request,'calculator/bmr.html',params)

def bmiCalculator(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = UserExtended.objects.get(user=request.user)
    if request.method == "POST":
        try:
            bmi = request.POST['bmi']
            Bmi.objects.filter(user=request.user).delete()
            Bmi.objects.create(
                user = request.user,
                bmi = bmi
            )
        except:
            messages.error(request,sys.exc_info()[0])
    params = {
        'user' : user,
        'dob' : ageCalculate(user.dob),
    }
    
    return render(request,'calculator/bmi.html',params)