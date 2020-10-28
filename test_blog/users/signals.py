from django.db.models.signals import post_save
from test_blog.blog.models import Blog
from .models import User


def user_saved(sender, instance, created, **kwargs):
    if created:
        blog = Blog(user=instance)
        blog.save()


post_save.connect(user_saved, sender=User)
