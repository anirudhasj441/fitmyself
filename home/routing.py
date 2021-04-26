from django.urls import path
from . import consumers
ws_pattern = [
    path('ws/notification_update/<slug>',consumers.NotificationUpdate.as_asgi()),
]