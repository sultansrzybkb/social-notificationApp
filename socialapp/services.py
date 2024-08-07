from actstream import action
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
class NotificationService:
    def create_comment_notification(self, comment):
        
        notification = {
            'type': 'notification',
            'message': f'New comment by {comment.user.username}: {comment.text}',
        }
       
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',  # Bildirim grubu
            {
                'type': 'notification_message',
                'message': notification['message'],
            }
        )
