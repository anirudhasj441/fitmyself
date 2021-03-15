from .models import UserExtended,ProfilePictures
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