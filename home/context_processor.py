from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from .models import UserExtended,ProfilePictures,Notification,Friend,FriendRequest


def user_profile(request):
    if request.user.is_authenticated:
        try:
            user = UserExtended.objects.get(user = request.user)
            user_profile = ProfilePictures.objects.filter(user=request.user).order_by("-upload_on").first()
            params = {
                "user" : user,
                "user_profile" : user_profile,
                "media" : settings.MEDIA_URL,
            }
        except ProfilePictures.DoesNotExist:
            params ={}
    else:
        params = {}
    return params

def search(request):
    if request.user.is_authenticated:
        if request.GET.get('search') is not None:
            result = {}
            profile_pics = []
            querry = request.GET.get('search')
            users = User.objects.filter(
                Q(first_name__icontains=querry) |
                Q(last_name__icontains=querry)
            )
            for user in users:
                result[UserExtended.objects.filter(user=user).first()] = ProfilePictures.objects.filter(user=user).order_by("-upload_on").first()
            params = {
                'result' : result,
            }
        else:
            params = {}
    else:
        params = {}
    return params

def notifications(request):
    if request.user.is_authenticated:
        friends = Friend.objects.filter(user = request.user)
        friend_users = []
        notification_profile_pic = {}
        for friend in friends:
            friend_users.append(friend.friends.user)
        notifications =  Notification.objects.filter(Q(user__in = friend_users) | Q(user=request.user)).order_by("-time")
        for notification in notifications:
            if notification.notification_type == 'post':
                notification_profile_pic[notification] = ProfilePictures.objects.filter(user = notification.user).order_by('-upload_on').first() 
            elif notification.notification_type == 'friend request':
                friend_request = FriendRequest.objects.get(slug = notification.friend_request.slug)
                friend_user = UserExtended.objects.get(slug = friend_request.sent_by.slug)
                notification_profile_pic[notification] = ProfilePictures.objects.filter(user = friend_user.user).order_by('-upload_on').first()
                # print(notification_profile_pic[notification])

        params = {
            'notifications' : notifications,
            'notification_profile_pic' : notification_profile_pic,
        }
    else:
        params = {}
    return params