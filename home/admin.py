from django.contrib import admin
from .models import UserExtended,ProfilePictures
# Register your models here.

class UserExtendedAdmin(admin.ModelAdmin):
    list_display = [
        'userPk',
        'name',
        'dob',
        'gender'
    ]
    def userPk(self,obj):
        return obj.user.pk
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = [
        'userPk',
        'name',
    ]
    def userPk(self,obj):
        return obj.user.pk
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

admin.site.register(UserExtended,UserExtendedAdmin)
admin.site.register(ProfilePictures,ProfilePictureAdmin)