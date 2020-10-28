from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.conf.urls import url
from django.views import defaults as default_views
from test_blog.blog.views import (BlogView, get_home_view,
                                  CreatePostView, get_post_view)
from test_blog.users.views import login_view, logout_view

urlpatterns = [
    path("", get_home_view, name="home"),
    # Django Admin, use {% url 'admin:index' %}
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("blog", login_required(BlogView.as_view()), name="blog"),
    url(r'^blog/(?P<type_feed>[^/.]+)/$',
        login_required(BlogView.as_view()), name='blog'),
    path(
        "blog/create-post",
        login_required(CreatePostView.as_view()), name="create_post"),
    url(r'^post/(?P<pk>[^/.]+)/$', get_post_view, name='post'),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
