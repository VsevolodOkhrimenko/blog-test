from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .forms import PostForm
from .models import Post, Blog


RESULT_PAGE_SIZE = 5


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.add_message(
                request, messages.SUCCESS, _('Post created successfully'))
            return redirect("blog")
    else:
        form = PostForm()
    return render(request, "pages/create_post.html", {'form': form})


@login_required
def get_blog_view(request, pk=None, type_feed=None):
    posts = Post.objects.all()
    if type_feed == 'my':
        posts = posts.filter(user=request.user)
    elif type_feed == 'personal':
        blogs = Blog.objects.filter(subscriptions__in=[request.user])
        posts = posts.filter(user__blog__in=blogs)
    paginator = Paginator(posts, RESULT_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
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
    return render(request, "pages/blog.html",
                  {'page_obj': page_obj, 'type_feed': type_feed})


@login_required
def get_post_view(request, pk=None):
    post = Post.objects.filter(pk=pk).first()
    return render(request, "pages/post.html", {"post": post})


def get_home_view(request):
    if request.user.is_authenticated:
        return redirect("blog")
    return render(request, "pages/home.html")
