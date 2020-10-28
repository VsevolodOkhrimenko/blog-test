from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from test_blog.blog.models import Post, Blog
from .serializers import PostSerializer

RESULT_PAGE_SIZE = 20

User = get_user_model()


class ResultsSetPagination(LimitOffsetPagination):
    default_limit = RESULT_PAGE_SIZE
    max_limit = RESULT_PAGE_SIZE
    template = None

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'results': data
        })


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = ResultsSetPagination

    def retrieve(self, request, pk=None):
        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            raise NotFound(detail=_("Error 404, page not found"), code=404)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def list(self, request):
        is_pesonal = request.GET.get('is_pesonal', None)
        my_posts = request.GET.get('my_posts', None)
        posts = self.queryset
        if is_pesonal:
            blogs = Blog.objects.filter(subscriptions__in=[request.user])
            posts = posts.filter(related_posts__in=blogs)
        if my_posts:
            posts = posts.filter(user=request.user)
        page = self.paginate_queryset(posts)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_subscription(self, request, pk):
        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            raise NotFound(detail="Error 404, page not found", code=404)
        blog = post.user.blog
        if blog.subscriptions.filter(pk=request.user).exists():
            blog.subscriptions.remove(request.user)
            return Response({
                'message': _('Successfully unsubscribed!'),
                'button_text': _('Subscribe')})
        blog.subscriptions.add(request.user)
        return Response({
            'message': _('Successfully subscribed!'),
            'button_text': _('Unsubscribe')})
