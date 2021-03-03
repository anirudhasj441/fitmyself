from .models import UserExtended,ProfilePictures
from django.contrib.auth.models import User
from django.conf import settings

def user_profile(request):
    if request.user.is_authenticated:
        try:
            user = ProfilePictures.objects.get(user=request.user)
            params = {
                "user_profile" : user,
                "media" : settings.MEDIA_URL
            }
        except ProfilePictures.DoesNotExist:
            params ={}
    else:
        params = []
    return params
