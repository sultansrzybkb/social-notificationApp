from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, PostViewSet, CommentViewSet

from  socialapp import views
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'notifications',NotificationViewSet,basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('home/', views.home, name='home'),
]
