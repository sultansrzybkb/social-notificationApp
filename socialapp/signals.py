from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from notifications.signals import notify
from actstream import action

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        action.send(instance.user, verb='commented on', target=instance.post, action_object=instance)
        if instance.user != instance.post.author:
            notify.send(instance.user, recipient=instance.post.author, verb='commented on your post', action_object=instance)