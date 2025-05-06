import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sujet_id = self.scope['url_route']['kwargs']['sujet_id']
        self.room_group_name = f"sujet_forum_{self.sujet_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope.get("user", None)

        await self.save_message(user, self.sujet_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message',
                'message': message,
                'sender': getattr(user, "username", "anonymous"),
                'date': str(datetime.now()),
            }
        )

    async def message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event.get('sender', "anonymous"),
            'date': event['date'],
        }))

    @database_sync_to_async
    def save_message(self, user, sujet_id, message):
        sujet_instance = sujets_forum.objects.get(sujet_id=sujet_id)
        return messages_forum.objects.create(
            sujet_id=sujet_instance,
            user_id=user if user and user.is_authenticated else None,
            contenu=message
        )

