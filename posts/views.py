from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from yatube.settings import PAGE_QUANITY

from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm


@cache_page(60, key_prefix="index_page")
def index(request):
    all_post = Post.objects.all()
    paginator = Paginator(all_post, PAGE_QUANITY)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page,
                                          "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, PAGE_QUANITY)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page,
                                          "paginator": paginator})


def groups_list(request):
    groups = Group.objects.order_by("title").all()
    paginator = Paginator(groups, PAGE_QUANITY)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group_list.html", {"groups": page,
                                               "paginator": paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "new_post.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    follower = user.follower.count()
    following = user.following.count()
    if request.user.is_authenticated:
        is_followed = Follow.objects.filter(user=request.user,
                                            author=user).exists()
    else:
        is_followed = None
    posts = user.posts.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"author": user,
                                            "user": request.user,
                                            "follower": follower,
                                            "following": following,
                                            "is_followed": is_followed,
                                            "post": posts,
                                            "page": page,
                                            "paginator": paginator})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    follower = user.follower.count()
    following = user.following.count()
    if request.user.is_authenticated:
        is_followed = Follow.objects.filter(user=request.user,
                                            author=user).exists()
    else:
        is_followed = None
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    return render(request, "post.html", {"author": user,
                                         "user": request.user,
                                         "follower": follower,
                                         "following": following,
                                         "is_followed": is_followed,
                                         "post": post,
                                         "comments": comments,
                                         "form": CommentForm()})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect("post", username, post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username, post_id)
    return render(request, "post_edit.html", {"form": form,
                                              "post": post})


@login_required
def add_comment(request, username, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect("post", username, post_id)


def page_not_found(request, exception=None):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    all_post = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(all_post, PAGE_QUANITY)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page,
                                           "paginator": paginator,
                                           "post": all_post})


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        return redirect("profile", username)
    Follow.objects.get_or_create(user=request.user, author=user)
    return redirect("profile", username)


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        return redirect("profile", username)
    Follow.objects.filter(user=request.user, author=user).delete()
    return redirect("profile", username)
