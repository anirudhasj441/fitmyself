from django.contrib import admin
from .models import Room,Message

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user_list',
    ]
    search_field = [
        'name',
    ]

class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'room_name',
        'msg',
        'media',
        'time',
        'seen',
    ]
    def name(self,obj):
        return str(obj.user.first_name)+" "+str(obj.user.last_name)
    def room_name(self,obj):
        return obj.room.name

admin.site.register(Room,RoomAdmin)
admin.site.register(Message,MessageAdmin)