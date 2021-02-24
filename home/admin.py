from django.contrib import admin
from .models import Workout,Exercie
# Register your models here.

class WorkoutAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "date",
        "parts",
    ]
    def name(self,obj):
        return obj.user.first_name+' '+obj.user.last_name

class ExerciseAdmin(admin.ModelAdmin):
    list_display = [
        "workout",
        "name",
        "repetition",
        "sets"
    ]

admin.site.register(Workout,WorkoutAdmin)
admin.site.register(Exercie,ExerciseAdmin)