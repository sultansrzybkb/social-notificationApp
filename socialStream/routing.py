from django.urls import path
from socialapp import consumer
websocket_urlpatterns = [
    path('ws/notifications/', consumer.NotificationConsumer.as_asgi()),
]