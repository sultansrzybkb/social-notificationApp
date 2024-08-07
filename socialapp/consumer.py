import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket bağlantısı açıldı.")
        self.group_name = 'notifications'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'notification_message',
                'message': data['message']
            }
        )

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))