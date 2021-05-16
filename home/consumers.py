from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json

# class AddNotification(WebsocketConsumer):
#     def connect(self):
#         self.room_name = 'add_notification'
#         self.room_group_name = 'noti'
#         print('Connect')
#         print(self.room_name)
#         print(self.room_group_name)
#         # async_to_sync(self.channel_layer.group_add)(
#         #     self.room_group_name,
#         #     self.channel_name
#         # )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

class NotificationUpdate(WebsocketConsumer):
    def connect(self):
        self.room_name = "notification-"+self.scope['url_route']['kwargs']['slug']
        self.room_group_name = "notifications"
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.send(text_data=json.dumps({
            'payload' : {'hello':'bye'},
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'notificationSend',
                'payload' : text_data
            }
        )

    def notificationSend(self, event):
        data = json.loads(event['values'])
        self.send(text_data = json.dumps({
            'payload' : 'hello'
        }))