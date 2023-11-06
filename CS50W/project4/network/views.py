import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import get_user
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import PostForm



from .models import Post, User, Follows, Like

def delete_like(request, post_id):
    post = Post.objects.get(pk = post_id)
    user = User.objects.get(pk = request.user.id)
    deleteLike = Like.objects.filter(user=user, post=post)
    deleteLike.delete()

def add_like(request, post_id):
    post = Post.objects.get(pk = post_id)
    user = User.objects.get(pk = request.user.id)
    addLike = Like(user=user, post=post)
    addLike.save()

def index(request):
    all_posts = Post.objects.all().order_by("-id")

    # pagination
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)

    likes = Like.objects.all()
    userLikedList = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                userLikedList.append(like.post.id)
    except:
        userLikedList=[]
            
    return render(request, "network/index.html", {
        "all_posts": all_posts, 
        "page_posts": page_posts, 
        "userLikedList": userLikedList
        
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = get_user(request)
        post=Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")

def profile(request, id):
    user = User.objects.get(pk=id)
    all_posts = Post.objects.filter(user=user).order_by("-id")

    following = Follows.objects.filter(user=user)
    followers = Follows.objects.filter(follows=user)

    checkIfFollow = followers.filter(user=User.objects.get(pk=request.user.id))
    # checkIfFollow = followers.filter(user=User.objects.get(pk=id))
    isFollowing = checkIfFollow.exists()
    
    

    # pagination
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)

    return render(request, "network/profile.html", {
        "all_posts": all_posts, 
        "page_posts": page_posts,
        "username": user.username,
        "following": following,
        "followers":followers,
        "isFollowing":isFollowing,
        "userprofile": user,
        "request": request
        
    })


def follow(request):
    user_to_follow = request.POST['user_to_follow']
    user = get_user(request)
    toFollowInfo = User.objects.get(username = user_to_follow)
    f = Follows(user=user, follows = toFollowInfo)
    f.save()
    user_id = toFollowInfo.id
    return HttpResponseRedirect(reverse("profile", kwargs={'id': user_id}))

def unfollow(request):
    user_to_unfollow = request.POST['user_to_unfollow']
    # user = get_user(request)
    user = User.objects.get(pk=request.user.id)
    toFollowInfo = User.objects.get(username = user_to_unfollow)
    f = Follows.objects.get(user=user, follows = toFollowInfo)
    f.delete()
    user_id = toFollowInfo.id
    return HttpResponseRedirect(reverse("profile", kwargs={'id': user_id}))

def following(request):
    user = get_user(request)
   
    following_users = Follows.objects.filter(user = user)
    all_posts = Post.objects.all().order_by("-id")

    following_users_posts = []

    for post in all_posts:
        for each in following_users:
            if each.follows == post.user:
                following_users_posts.append(post)
     # pagination
    paginator = Paginator(following_users_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)

    return render(request, "network/following.html", {
        "page_posts": page_posts,
   
    })

def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        required_post = Post.objects.get(pk=post_id)
        required_post.content = data["content"]
        required_post.save()
        return JsonResponse({"message": "edited"})



