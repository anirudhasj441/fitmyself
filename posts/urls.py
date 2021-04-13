from django.urls import path
from . import views

urlpatterns = [
    path('add_post',views.addPost,name="add_post"),
    path('comment/<str:slug>',views.comment,name="comment"),
]
