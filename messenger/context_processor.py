from django.contrib.auth.models import User
from home.models import UserExtended, ProfilePictures,Friend

def chatUser(request):
    if request.user.is_authenticated:
        chat_friends = Friend.objects.filter(user=request.user)
        chat_friend_profile_pic = {}
        for friend in chat_friends:
            print(friend.friends.user.first_name)
            chat_friend_profile_pic[friend] = ProfilePictures.objects.filter(user = friend.friends.user).order_by('-upload_on').first()
        params = {
            'chat_friends' : chat_friends,
            'chat_friend_profile_pic' : chat_friend_profile_pic,
        }
    else:
        params = {}
    return params


