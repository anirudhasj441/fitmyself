from django.urls import path
from . import consumers

ws_pattern2 = [
    path('ws/messenger/chat/<name>',consumers.Messenger.as_asgi()),
]