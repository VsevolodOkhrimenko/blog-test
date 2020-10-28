from rest_framework.serializers import ModelSerializer
from test_blog.blog.models import Post


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'header',
            'text',
            'created',
            'user',
        )
