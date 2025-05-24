import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import sujets_forum, messages_forum
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
        message_type = data.get('type', 'message')
        user = self.scope.get("user", None)
        message_id = data.get('message_id', None)

        if message_type == 'audio':
            audio_url = data['audio_url'] 
            audio_relative_path = audio_url.split("/media")[-1]
            audio_path = f"/media{audio_relative_path}"
            update_message = await self.update_message(user, message_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'message': audio_path,
                    'sender': getattr(user, "username", "anonymous"),
                    'date': str(datetime.now()),
                    'is_audio': True,
                }
            )

        elif message_type == 'message':
            message = data['message']
            saved_msg = await self.save_message(user, self.sujet_id, message, is_audio=False)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'message_id': str(saved_msg.message_id),
                    'message': message,
                    'sender': getattr(user, "username", "anonymous"),
                    'date': str(saved_msg.date_message),
                    'is_audio': False,
                }
            )

    async def message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event.get('sender', "anonymous"),
            'date': event['date'],
            'is_audio': event.get('is_audio', False),
        }))

    @database_sync_to_async
    def save_message(self, user, sujet_id, content, is_audio=False):
        sujet_instance = sujets_forum.objects.get(sujet_id=sujet_id)
        return messages_forum.objects.create(
            sujet_id=sujet_instance,
            user_id=user if user and user.is_authenticated else None,
            contenu="Audio message" if is_audio else content,
            audio=content if is_audio else None
        )
    @database_sync_to_async
    def update_message(self, user,message_id):
        message_instance = messages_forum.objects.get(message_id=message_id)
        message_instance.user_id = user if user and user.is_authenticated else None
        message_instance.save()
