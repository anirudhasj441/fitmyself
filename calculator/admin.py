from django.contrib import admin
from .models import Bmi,Bmr

# Register your models here.

class BmrAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "bmr",
        "date_filled",
    ]
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

class BmiAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "bmi",
        "date_filled",
    ]
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

admin.site.register(Bmi,BmiAdmin)
admin.site.register(Bmr,BmrAdmin)