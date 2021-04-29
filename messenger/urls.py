from django.urls import path
from . import views

urlpatterns = [
    path('',views.messenger,name='messenger'),
    path('create_room/<str:slug>',views.createRoom,name='create_room'),
    path('chat/<str:name>',views.chat,name='chat'),
]