from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from authenticate.models import Follower
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error




# Create your views here.

def home(request):
    return HttpResponse('ok')

@login_required(login_url='home')
def addPost(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text',None)
        video = None
        video = request.FILES.get('video', None)
        images = request.FILES.getlist('images', None)
        post = Post(user = user, text = text, video = video )
        post.save()
        for image in images:
            name = f'{user.username} posted "{text[0:20]}" '
            postImage = Image(image = image, name = name)
            postImage.save()
            post.images.add(postImage)
        if text is None and video is None:
            post.delete()
            error(request,'cannot post an empty post' )
            return redirect('add_post')
        post.save()
        return redirect('home')
    return render(request, 'posts/addPost.html')

@login_required(login_url='home')
def posts(request):
    following = Follower.objects.filter(follower = request.user)
    posts = Post.objects.filter(user = request.user)
    likes = []
    try:
        likes = Like.objects.filter(user = request.user)
    except:
        pass
    likedPosts = [like.post for like in likes]

    for user in following:
        userPosts = Post.objects.filter(user = user.user)
        posts = list(posts) + list(userPosts) 
    posts = list(posts)
    posts.sort(key=lambda x: x.created, reverse=True)
    context = {'posts':posts, 'likes': likedPosts}
    return render(request,'posts/posts.html', context)

@login_required(login_url='home')
def post(request,pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post__id = post.id)
    likes = Like.objects.filter(post__id = post.id)
    liked = False
    for like in likes:
        if like.user == request.user:
            liked = True
            break

    if request.method == 'POST':
        text = request.POST['comment']
        comment = Comment(user = request.user, text=text, post = post)
        comment.save()
        post.comment += 1
        post.save()
    context = {'post':post, 'comments':comments, 'likes':likes, 'liked':liked}
    return render(request, 'posts/post.html', context)

@login_required(login_url='home')
def like(request, pk):
    post = Post.objects.get(id=pk)
    post.like += 1
    post.save()
    liked = Like(user = request.user, post = post)
    liked.save()
    return redirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.path)

@login_required(login_url='home')
def unlike(request,pk):
    post = Post.objects.get(id = pk)
    like = Like.objects.get(post__id = pk , user = request.user)
    post.like -= 1
    post.save()
    like.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='home')
def deletePost(request, pk):
    if request.method == 'POST':

        post = Post.objects.get(id=pk)
        post.delete()
        return redirect('posts')
    return render(request, 'posts/delete.html')

@login_required(login_url='home')
def deleteComment(request, pk):
    if request.method == 'POST':

        comment = Comment.objects.get(id=pk)
        post = comment.post
        post.comment -= 1
        post.save()
        comment.delete()
        return redirect('post', pk=post.id)
    return render(request, 'posts/delete.html')

@login_required(login_url='login')
def editPost(request,pk):
    post = Post.objects.get(id = pk)
    if request.method == 'POST':
        post.text = request.POST.get('text')
        if request.FILES.get('video') is not None:
            post.video = request.FILES.get('video')
        images = request.FILES.getlist('images')
        post.save()
        for image in images:
            name = f'{request.user.username} edited "{post.text[0:20]}" '
            postImage = Image(image = image, name = name)
            postImage.save()
            post.images.add(postImage)
        post.save()
        return redirect('home')
    
    context = {'post':post}
    return render(request, 'posts/addPost.html', context)

@login_required(login_url='login')
def viewComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        reply = Reply(user = request.user, comment = comment, text = text)
        reply.save()
        comment.replies += 1
        comment.save()
    
    replies = Reply.objects.filter(comment = comment)
    context = {'comment': comment, 'replies':replies}
    return render(request, 'posts/comment.html', context)

@login_required(login_url='login')
def deleteReply(request, pk):
    if request.method == 'POST':
        reply = Reply.objects.get(id = pk)
        reply.delete()
        return redirect('comment', pk = reply.comment.id)
    return render(request, 'posts/delete.html')
    
            
