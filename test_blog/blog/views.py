from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from .forms import PostForm
from .models import Post, Blog


RESULT_PAGE_SIZE = 20


class CreatePostView(View):
    form = PostForm
    template = "pages/create_post.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.add_message(
                request, messages.SUCCESS, _('Post created successfully'))
            return redirect("blog")
        return render(request, self.template, {'form': form})


class BlogView(View):
    template = "pages/blog.html"
    posts = Post.objects.all()

    def get(self, request, type_feed=None, *args, **kwargs):
        posts = self.posts
        if type_feed == 'my':
            posts = posts.filter(user=request.user)
        elif type_feed == 'personal':
            blogs = Blog.objects.filter(subscriptions__in=[request.user])
            posts = posts.filter(user__blog__in=blogs)
        paginator = Paginator(posts, RESULT_PAGE_SIZE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template,
                      {'page_obj': page_obj, 'type_feed': type_feed})

    def post(self, request, type_feed=None, *args, **kwargs):
        action = request.POST['action']
        if action == 'unsubscribe':
            blog_id = request.POST['blog']
            blog = get_object_or_404(Blog, pk=blog_id)
            messages.add_message(
                request, messages.SUCCESS, _('Successfully unsubscribed'))
            blog.subscriptions.remove(request.user)
        elif action == 'subscribe':
            blog_id = request.POST['blog']
            blog = get_object_or_404(Blog, pk=blog_id)
            messages.add_message(
                request, messages.SUCCESS, _('Successfully subscribed'))
            blog.subscriptions.add(request.user)
        elif action == 'notseen':
            post_id = request.POST['post']
            post = get_object_or_404(Post, pk=post_id)
            post.seen.remove(request.user)
            messages.add_message(
                request, messages.SUCCESS, _('Successfully unseen'))
        elif action == 'seen':
            post_id = request.POST['post']
            post = get_object_or_404(Post, pk=post_id)
            post.seen.add(request.user)
            messages.add_message(
                request, messages.SUCCESS, _('Successfully seen'))
        return self.get(request, type_feed, args, kwargs)


@login_required
def get_post_view(request, pk=None):
    post = Post.objects.filter(pk=pk).first()
    return render(request, "pages/post.html", {"post": post})


def get_home_view(request):
    if request.user.is_authenticated:
        return redirect("blog")
    return render(request, "pages/home.html")
