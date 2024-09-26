from django.shortcuts import render
from .models import *
from django.db.models import Q

# Create your views here.
def chats(request):
    user = request.user
    page = 'chats'
    messages = Message.objects.filter(Q(sender = user) | Q(receiver = user))
    chats = {}
    users = [message.sender if  message.sender != user else message.receiver for message in messages ]
    for message in messages:
        if message.sender != user:
            chats.update({message.sender:message}) 
        else:
            chats.update({message.receiver:message})
    context = {'users':users, 'chats':chats,'page':page}
    return render(request, 'message/chats.html', context)

def chat(request, pk):
    user = User.objects.get(id = pk)
    messages = Message.objects.filter(Q(sender = user, receiver = request.user) | Q(receiver = user, sender = request.user))
    for message in messages:
        message.read = True
        message.save()
    context = {'messages':messages,'user':user}
    return render(request, 'message/chat.html', context)
