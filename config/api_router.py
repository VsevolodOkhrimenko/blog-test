from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from test_blog.blog.api.views import PostViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("posts", PostViewSet)


app_name = "api"
urlpatterns = router.urls
