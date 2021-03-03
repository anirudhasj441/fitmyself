from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Workout,Exercie
import sys

def listToString(list):
    string = ""
    for items in list:
        string += items.capitalize()+","
    return string[:-1]

# Create your views here.
def addWorkouts(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        try:
            date = request.POST['date']
            parts = request.POST.getlist('parts')
            print(listToString(parts))
            workout = Workout.objects.create(
                user = request.user,
                date = date,
                parts = listToString(parts),
            )
        except:
            messages.error(request,sys.exc_info()[0])
        else:
            return redirect('/workout/add_exercise/'+str(workout.pk))
    return render(request,"workout/add_workout.html")

def addExercise(request):
    if not request.user.is_authenticated:
        return redirect('/')

    return render(request,'workout/add_exercise.html')