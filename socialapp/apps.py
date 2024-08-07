from django.apps import AppConfig
class SocialappConfig(AppConfig):
    name = 'socialapp'

    def ready(self):
        import socialapp.signals
        from actstream import registry
        from .models import Post, Comment
        registry.register(Post)
        registry.register(Comment)