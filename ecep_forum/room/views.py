from django.shortcuts import render,redirect

from .models import *

from django.contrib.auth.decorators import login_required


@login_required
def rooms(request):
    """ Liste des groupe de chat """
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    """ Details groupe de chat """
    room = Room.objects.get(slug=slug)    
    messages = Message.objects.filter(room=room)[0:30]
    return render(request, 'room/room.html', {'room': room, 'messages':messages})


@login_required
def add_message(request, slug):
    """ Ajout d'un message dans un groupe de chat """
    room = Room.objects.get(slug=slug)
    message = request.POST.get('message')
    Message.objects.create(user=request.user, room=room, content=message)
    return redirect('room', slug=slug)