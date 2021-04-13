from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json

class AddNotification(WebsocketConsumer):
    def connect(self):
        self.room_name = 'add_notification'
        self.room_group_name = 'noti'
        print('Connect')
        print(self.room_name)
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )