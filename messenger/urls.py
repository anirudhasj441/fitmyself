from django.urls import path
from . import views

urlpatterns = [
    path('',views.messenger,name='messenger'),
    # path('chat/<str:room>',views.chat,name='chat'),
]