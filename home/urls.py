from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.userLogut,name='logout'),
    path('user/<str:slug>',views.userProfilePage,name='profile'),
    path('user/<str:slug>/photos',views.userPhotos,name='photos'),
    path('edit-profile-pic/<str:slug>',views.uploadProfilePic,name='edit-profile-pic'),
    path('edit-cover-pic/<str:slug>',views.uploadCoverPic,name='edit-cover-pic'),
    path('request/<str:slug>',views.sendFriendRequest,name='sent-friend-request'),
    path('cancel-request/<str:slug>',views.cancelRequest,name='cancel-request'),
    path('delete-request/<str:slug>',views.deleteRequest,name='delete-request'),
    path('accept-request/<str:slug>',views.acceptRequest,name='accept-request'),
    path('like/<str:slug>',views.likePost,name='like'),
    path('unlike/<str:slug>',views.unlikePost,name='unlike'),
]