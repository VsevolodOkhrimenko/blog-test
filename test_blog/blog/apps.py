from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'test_blog.blog'

    def ready(self):
        try:
            import test_blog.blog.signals  # noqa F401
        except ImportError:
            pass
