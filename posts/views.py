from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Like, Comment, Image
from authenticate.models import Follower
from django.contrib.auth.decorators import login_required




# Create your views here.

def home(request):
    return HttpResponse('ok')

login_required(login_url='home')
def addPost(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text',None)
        video = None
        video = request.FILES.get('video', None)
        images = request.FILES.getlist('images')
        post = Post(user = user, text = text, video = video )
        post.save()
        for image in images:
            name = f'{user.username} posted "{text[0:20]}" '
            postImage = Image(image = image, name = name)
            postImage.save()
            post.images.add(postImage)
        post.save()
        return redirect('home')
    return render(request, 'posts/addPost.html')

login_required(login_url='home')
def posts(request):
    following = Follower.objects.filter(follower = request.user)
    posts = Post.objects.filter(user = request.user)
    for user in following:
        userPosts = Post.objects.filter(user = user.user)
        posts = list(posts) + list(userPosts) 
    posts = list(posts)
    posts.sort(key=lambda x: x.created, reverse=True)
    context = {'posts':posts}
    return render(request,'posts/posts.html', context)

def post(request,pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post__id = post.id)
    likes = Like.objects.filter(post__id = post.id)

    if request.method == 'POST':
        text = request.POST['comment']
        comment = Comment(user = request.user, text=text, post = post)
        comment.save()
    context = {'post':post, 'comments':comments, 'likes':likes}
    return render(request, 'posts/post.html', context)

def like(request, pk):
    post = Post.objects.get(id=pk)
    post.like += 1
    post.save()
    liked = Like(user = request.user, post = post)
    liked.save()
    return redirect(request.META.get('HTTP_REFERER'))

def unlike(request,pk):
    
    post = Post.objects.get(id = pk)
    like = Like.objects.get(post__id = pk , user = request.user)
    post.like -= 1
    post.save()
    like.delete()
    return redirect(request.META.get('HTTP_REFERER'))
            
