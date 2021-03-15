from django.urls import path
from . import views

urlpatterns = [
    path('',views.workout,name='workout'),
    path('add_workout',views.addWorkouts,name='add_workout'),
    path('add_exercise/<str:slug>',views.addExercise,name='add_exersice'),
    path('update_workout/<str:slug>',views.updateWorkout,name='update_workout'),
    # APIs
    path('update_exercise/<str:slug>/<int:id>',views.updateExercise,name='update_exercise'),
    path('delete_workout/<str:slug>',views.deleteWorkout,name='delete_workout'),
    path('delete_exercise/<str:slug>/<int:id>',views.deleteExercise,name='delete_exercise'),
]