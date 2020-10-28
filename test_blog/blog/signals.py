from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from .models import Post

FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


def post_saved(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.user.blog.subscriptions.all().exclude(
            email__isnull=True).exclude(
            email='')
        emails = subscribers.values_list('email', flat=True).distinct()
        message = "New post with header {} was published!".format(
            instance.header)
        for email in emails:
            send_mail(message, message, FROM_EMAIL, [email])


post_save.connect(post_saved, sender=Post)
