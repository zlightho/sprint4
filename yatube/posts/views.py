from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from posts.forms import PostForm

from .models import Post, Group, User


def paginator(posts, request):
    paginator = Paginator(posts, settings.PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return {
        "paginator": paginator,
        "page_obj": page_obj,
        "page_number": page_number,
    }


def index(request):
    context = paginator(Post.objects.all(), request)
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        "group": group,
        "posts": posts,
    }
    context.update(paginator(posts, request))
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    context = {
        "author": author,
    }
    context.update(paginator(posts, request))
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        "post": post,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_edit(request, post_id):
    groups = Group.objects.all()
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post.pk)
    context = {"is_edit": True, "post": post, "form": form, "groups": groups}
    return render(request, "posts/create_post.html  ui", context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username=request.user)
    context = {"is_edit": False, "form": form, "groups": groups}
    return render(request, "posts/create_post.html", context)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=200)
