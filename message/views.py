from django.shortcuts import render
from .models import *
from django.db.models import Q

# Create your views here.
def chats(request):
    user = request.user
    page = 'chats'
    messages = (Message.objects.filter(Q(sender = user) | Q(receiver = user)))
    # messages.sort(key = lambda  x: x.created, reverse=True)
    chats = {}
    for message in messages:
        if message.sender != user:
            try:
                chats.pop(message.sender)
                chats[message.sender]= message 
            except:
                chats[message.sender]= message
        else:
            try:
                chats[message.receiver]=message
                chats.pop(message.sender)
            except:
                chats[message.receiver]=message
    # chats = dict(sorted(list(chats.items())), key = lambda x : x[1].created)

    context = { 'chats':chats,'page':page}
    return render(request, 'message/chats.html', context)

def chat(request, pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        message = Message(text = text, sender = request.user, receiver = user)
        message.save()
    messages = Message.objects.filter(Q(sender = user, receiver = request.user) | Q(receiver = user, sender = request.user))
    
    for message in messages:
        if message.sender != request.user:
            message.read = True
            message.save()
    
    room_name = Message.getRoomName(user, request.user)
    
    context = {'messages':messages,'user':user, 'room_name':room_name}
    return render(request, 'message/chat.html', context)
