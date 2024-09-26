import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from message.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.load(text_data)
        message = text_data_json

        print(message)
    

    '''
    async def send_message(self, event):
        data = event['message']
        await self.create_message(data= data)
        response = {
            'sender':data['sender'],
            'message':data['message'],
            'receiver':data['receiver'],

        }
        await self.send(text_data = json.dump({'message':response}))
    
    @database_sync_to_async
    def create_message(self, data):
        # get_room_name = Message.getRoomName(data['sender'], data['receiver'])
        if not Message.objects.filter(message = data['message']).exists():
            # sender = User.objects.get(username = data['sender'].username)
            # reciever = User.objects.get(username = data['reciever'].username)
            new_message = Message(text = data['message'], sender=data['sender'], receiver = data['receiver'])
            new_message.save()

            '''