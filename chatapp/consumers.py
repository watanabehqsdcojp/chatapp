import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        messages = await sync_to_async(self.get_message_list, thread_sensitive=True)()

        await self.accept()
        await self.send(text_data=json.dumps({
            'messages': messages
        }, cls=DjangoJSONEncoder))

    def get_message_list(self):
        room = get_object_or_404(Room, pk=self.room_name)
        messages = Message.objects.filter(room=room).values('text', 'speaker', 'created_at')
        return list(messages)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        room = await sync_to_async(get_object_or_404, thread_sensitive=True)(
            Room, pk=self.room_name
        )

        await sync_to_async(Message.objects.create, thread_sensitive=True)(
            text=message,
            speaker=self.user,
            room=room
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))