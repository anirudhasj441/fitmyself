from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.userLogut,name='logout'),
    path('<str:slug>',views.userProfile,name='profile'),
    path('edit-profile-pic/<str:slug>',views.uploadProfilePic,name='edit-profile-pic'),
    path('edit-cover-pic/<str:slug>',views.uploadCoverPic,name='edit-cover-pic'),
]