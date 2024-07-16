import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Comment, Like, Post, Scrap


def home(request):
    posts = Post.objects.all()
    return render(request, 'blogs.html', {'posts': posts})


@login_required(login_url='/registration/login')
def new(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user
        )
        return redirect('detail', new_post.slug)
    return render(request, 'new-post.html')


def detail(request, slug):
    post = Post.objects.get(slug=slug)
    user_has_liked = Like.objects.filter(user=request.user, post=post).exists(
    ) if request.user.is_authenticated else False
    user_has_scraped = Scrap.objects.filter(user=request.user, post=post).exists(
    ) if request.user.is_authenticated else False

    if (request.method == 'POST'):
        Comment.objects.create(
            post=post,
            content=request.POST['content'],
            author=request.user
        )
        return redirect('detail', slug)

    context = {
        'post': post,
        'user_has_liked': user_has_liked,
        'user_has_scraped': user_has_scraped,
    }
    return render(request, 'detail.html', context)


@login_required
def edit(request, slug):
    if request.user != Post.objects.get(pk=slug).author:
        return redirect('home')
    post = Post.objects.get(pk=slug)

    if request.method == 'POST':
        Post.objects.filter(pk=slug).update(
            title=request.POST['title'],
            content=request.POST['content']
        )
        return redirect('detail', slug)

    return render(request, 'edit.html', {'post': post})


def delete(request, slug):
    post = Post.objects.get(pk=slug)
    post.delete()
    return redirect('home')


def delete_comment(request, slug, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('detail', slug)


def signup(request):
    if (request.method == 'POST'):
        found_user = User.objects.filter(username=request.POST['username'])
        if (len(found_user) > 0):
            error = 'username already exits'
            context = {'error': error}
            return render(request, 'registration/signup.html', context)

        new_user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        auth.login(
            request,
            new_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect('home')

    return render(request, 'registration/signup.html')


def login(request):
    if (request.method == 'POST'):
        found_user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if (found_user is None):
            error = "username or password is incorrect"
            return render(request, 'registration/login.html', {'error': error})
        auth.login(
            request,
            found_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect(request.GET.get('next', '/'))
    return render(request, 'registration/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def mypage(request):
    likes = Like.objects.filter(user=request.user).select_related('post')
    scraps = Scrap.objects.filter(user=request.user).select_related('post')
    user_posts = Post.objects.filter(author=request.user)
    context = {
        "likes": likes,
        "scraps": scraps,
        "user_posts": user_posts
    }
    return render(request, 'mypage.html', context)


@login_required
def liked_posts(request):
    likes = Like.objects.filter(user=request.user).select_related('post')
    liked_posts = [like.post for like in likes]
    title = "liked"
    context = {"posts": liked_posts, "title": title}
    return render(request, 'liked_posts.html', context)


@login_required
def myposts(request):
    posts = Post.objects.filter(author=request.user)
    title = "liked"
    context = {"posts": posts, "title": title}
    return render(request, 'mypost.html', context)


@login_required
def saved_posts(request):
    scraps = Scrap.objects.filter(user=request.user).select_related('post')
    scraped_posts = [scrap.post for scrap in scraps]
    title = "saved"
    context = {"posts": scraped_posts, "title": title}
    return render(request, 'liked_posts.html', context)


# def mypage(request):
#     posts = Post.objects.all()
#     likes = Like.objects.filter(user=request.user)
#     scraps = Scrap.objects.filter(user=request.user)
#
#     context = {"posts": posts, "scraps": scraps, "likes": likes}
#     return render(request, 'mypage.html', context)


@csrf_exempt
def like(request):
    print("view like")
    if request.method == "POST":
        request_body = json.loads(request.body)
        print(request_body)
        post_pk = request_body["post_pk"]

        existing_like = Like.objects.filter(
            post=Post.objects.get(pk=post_pk),
            user=request.user
        )

        if existing_like.count() > 0:
            existing_like.delete()
        else:
            Like.objects.create(
                post=Post.objects.get(pk=post_pk),
                user=request.user
            )

        post_likes = Like.objects.filter(
            post=Post.objects.get(pk=post_pk)
        )

        response = {
            'like_count': post_likes.count(),
            'existing_like': existing_like.count(),
        }

        return HttpResponse(json.dumps(response))


@csrf_exempt
def scrap(request):
    if request.method == "POST":
        request_body = json.loads(request.body)

        post_pk = request_body["post_pk"]

        existing_scrap = Scrap.objects.filter(
            post=Post.objects.get(pk=post_pk),
            user=request.user
        )

        if existing_scrap.count() > 0:
            existing_scrap.delete()
        else:
            Scrap.objects.create(
                post=Post.objects.get(pk=post_pk),
                user=request.user
            )

        post_scraps = Scrap.objects.filter(
            post=Post.objects.get(pk=post_pk)
        )

        response = {
            'scrap_count': post_scraps.count(),
        }

        return HttpResponse(json.dumps(response))
