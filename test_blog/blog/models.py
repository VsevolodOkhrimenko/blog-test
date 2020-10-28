import uuid
from django.contrib.auth import get_user_model
from django.db.models import (Model, UUIDField, ForeignKey, DateTimeField,
                              ManyToManyField, OneToOneField, TextField,
                              CharField, SET_NULL)


User = get_user_model()


class Blog(Model):

    class Meta:
        ordering = ('user', 'created')

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=SET_NULL)
    subscriptions = ManyToManyField(
        User, blank=True, related_name='subscribed_users')
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.created)


class Post(Model):

    class Meta:
        ordering = ('-created', 'user',)

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=SET_NULL)
    header = CharField(max_length=128)
    text = TextField(max_length=2048)
    seen = ManyToManyField(User, blank=True, related_name='seen_posts')
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.created)
