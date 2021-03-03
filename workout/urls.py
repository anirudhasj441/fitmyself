from django.urls import path
from . import views

urlpatterns = [
    path('add_workout',views.addWorkouts,name='add_workout'),
    path('add_exercise',views.addExercise,name='add_exersice'),
]