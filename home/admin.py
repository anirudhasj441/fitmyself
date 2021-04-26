from django.contrib import admin
from .models import UserExtended,ProfilePictures,CoverPicture,Friend,FriendRequest,Notification
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
        'display_picture',
        'upload_on',
    ]
    list_filter = [
        'user'
    ]

    def userPk(self,obj):
        return obj.user.pk
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

class CoverPictureAdmin(admin.ModelAdmin):
    list_display = [
        'userPk',
        'name',
    ]
    list_filter = [
        'user'
    ]
    def userPk(self,obj):
        return obj.user.pk
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

class FriendAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user_name',
        'friend_name',
    ]
    def user_name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name
    def friend_name(self,obj):
        return obj.friends.user.first_name+" "+obj.friends.user.last_name

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "user_name",
        "sent_user",
        "time",
        "accepted",
    ]
    def user_name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name
    def sent_user(self,obj):
        return obj.sent_by.user.first_name+" "+obj.sent_by.user.last_name

class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "time",
        "notification_type",
        "seen",
    ]
    list_filter = [
        'notification_type',
        'seen'
    ]
    list_per_page = 10
    def name(self,obj):
        return obj.user.first_name +" "+ obj.user.last_name

admin.site.register(UserExtended,UserExtendedAdmin)
admin.site.register(ProfilePictures,ProfilePictureAdmin)
admin.site.register(CoverPicture,CoverPictureAdmin)
admin.site.register(Friend,FriendAdmin)
admin.site.register(FriendRequest,FriendRequestAdmin)
admin.site.register(Notification,NotificationAdmin)
