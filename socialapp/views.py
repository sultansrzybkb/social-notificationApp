from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from socialapp.serializers import PostSerializer, CommentSerializer
from honeypot.decorators import check_honeypot
from django.contrib.auth.models import User
from notifications.signals import notify
from actstream import action as actstream_action
from notifications.models import Notification
from rest_framework.permissions import AllowAny
from .serializers import NotificationSerializer
from .utils import send_websocket_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        actstream_action.send(self.request.user, verb='created post', target=post)

              # WebSocket bildirimi gönderme
        send_websocket_notification(self.request.user.id, f"New post created by {self.request.user.username}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
       

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
  

    @check_honeypot
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user)
            post = comment.post
            actstream_action.send(request.user, verb='commented on', target=post, action_object=comment)
            notify.send(request.user, recipient=post.author, verb='commented on your post', target=post, action_object=comment)
            
            send_websocket_notification(post.author.id, f"{request.user.username} commented on your post")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
 
class ActivityViewSet(viewsets.ModelViewSet):
    queryset =action


def home(request):
    return render(request, 'home.html')