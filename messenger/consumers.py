from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .views import getMessage 
import json

class Messenger(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['name']
        self.room_group_name = 'message.'+str(self.room_name)
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('chat room connect')

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
            'type' : 'sendMessege',
            'payload' : text_data
        })

    def sendMessege(self, event):
        data = json.loads(event['values'])
        self.send(text_data = json.dumps({
            'payload' : getMessage(self.room_name)
        }))
