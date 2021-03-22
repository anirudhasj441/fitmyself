from .models import Post,Like,Comment
from home.models import ProfilePictures

def posts(request):
    if not request.user.is_authenticated:
        params = {}
    profile_pictures = {}
    posts = Post.objects.filter(user = request.user)
    for post in posts:
        profile_pictures[post] = ProfilePictures.objects.filter(user=post.user).order_by("-upload_on").first()
    params = {
        'posts' : posts,
        'post_profile_pictures' : profile_pictures,
    }
    return params
