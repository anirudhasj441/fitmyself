from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Workout,Exercise
from datetime import datetime
import sys

def listToString(list):
    string = ""
    for items in list:
        string += items.capitalize()+","
    return string[:-1]

def StringToList(string):
    return string.lower().split(",")

# Create your views here.
def workout(request):
    if not request.user.is_authenticated:
        return redirect('/')
    page = request.GET.get('page',1)
    exercises = []
    workout_list = Workout.objects.filter(user = request.user).order_by("-date")
    paginator = Paginator(workout_list,2)
    try:
        workouts = paginator.page(page)
    except PageNotAnInteger:
        workouts = paginator.page(1)
    except EmptyPage:
        workouts = paginator.page(paginator.num_pages)
    for workout in workout_list:
        exercises.append(Exercise.objects.filter(workout=workout))
    params = {
        'workouts' : workouts,
        'exercises' : exercises,
    }
    return render(request,'workout/workout.html',params)

def addWorkouts(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        try:
            date = request.POST['date']
            parts = request.POST.getlist('parts')
            slug = request.user.first_name+"-"+request.user.last_name+"-"+str(datetime.now())
            workout = Workout.objects.create(
                user = request.user,
                date = date,
                parts = listToString(parts),
                slug = slug,
            )
        except:
            messages.error(request,sys.exc_info()[0])
        else:
            return redirect('/workout/add_exercise/'+str(workout.slug))
    return render(request,"workout/add_workout.html")

def addExercise(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        workout = Workout.objects.get(slug=slug)
        exercises = Exercise.objects.filter(workout=workout)
        if request.method == "POST":
            name = request.POST["name"]
            repetition = request.POST["repetition"]
            sets = request.POST["sets"]
            if not sets.isnumeric():
                raise ValueError
            exersice = Exercise.objects.create(
                workout = workout,
                name = name,
                repetition = repetition,
                sets = sets,
            )
    except ValueError:
        return HttpResponse("<script>alert('Sets and Repetition should number')</script>")
    except Workout.DoesNotExist:
        return redirect('/workout/add_workout')
    params = {
        "workout":workout,
        "exercises":exercises,
    }
    return render(request,'workout/add_exercise.html',params)

def updateWorkout(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    workout = Workout.objects.get(slug=slug)
    if request.method == "POST":
        try:
            date = request.POST["date"]
            parts = request.POST.getlist("parts")
            workout.date = date
            workout.parts = listToString(parts)
            print("here"+workout.slug)
            workout.save()
        except:
            messages.error(request,sys.exc_info()[0])
        else:
            return redirect('/workout/add_exercise/'+str(workout.slug))
    params = {
        'workout' : workout,
        "parts" : StringToList(workout.parts)
    }
    return render(request,'workout/update_workout.html',params)

# APIs

def updateExercise(request,slug,id):
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        workout = Workout.objects.get(slug=slug)
        exercise = Exercise.objects.get(pk=id)
        if request.method == "POST":
            name = request.POST["name"]
            repetition = request.POST["repetition"]
            sets = request.POST["sets"]
            exercise.name = name
            exercise.repetition = repetition
            exercise.sets = sets
            exercise.save()
    except:
        messages.error(request,sys.exc_info()[0])
    else:
        return redirect('/workout/add_exercise/'+str(workout.slug))

def deleteWorkout(request,slug):
    if not request.user.is_authenticated:
        return redirect('/')
    workout = Workout.objects.get(slug=slug).delete()
    return redirect('/workout')
    
def deleteExercise(request,slug,id):
    if not request.user.is_authenticated:
        return redirect('/')
    exercise = Exercise.objects.get(pk=id).delete()
    workout = Workout.objects.get(slug=slug)
    return redirect('/workout/add_exercise/'+workout.slug)
    