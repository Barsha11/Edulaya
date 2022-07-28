import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage, Thread
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({'status':'connected','type':'text_message'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('msg_type') =='text_message':
            message = text_data_json['message']

            sent_by_id = text_data_json.get('sent_by')
            send_to_id = text_data_json.get('send_to')
            thread_id = text_data_json.get('thread_id')

            if not message:
                print('Error:: empty message')
                return False

            sent_by_user =await self.get_user_object(sent_by_id)
            send_to_user =await self.get_user_object(send_to_id)
            thread_obj =await self.get_thread(thread_id)
            if not sent_by_user:
                print('Error:: sent by user is incorrect')
            if not send_to_user:
                print('Error:: send to user is incorrect')
            if not thread_obj:
                print('Error:: Thread id is incorrect')
            # Create ChatMessage object
            await self.create_chat_message(thread_obj, sent_by_user, message)


            other_user_chat_room = f'chat_{send_to_id}'
            self_user = self.scope['user']
            response = {
                'message': message,
                'sent_by': self_user.id,
                'thread_id': thread_id
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

    async def chat_message(self, event):
        print('message', event)
        await self.send(json.dumps({
            'type': 'websocket.send',
            'text': event
        }))



    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, message):
        ChatMessage.objects.create(thread=thread, user=user, message=message)


