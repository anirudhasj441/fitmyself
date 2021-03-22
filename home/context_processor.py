from .models import UserExtended,ProfilePictures
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings

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
            print(result)
            params = {
                'result' : result,
            }
        else:
            params = {}
    else:
        params = {}
    return params
        