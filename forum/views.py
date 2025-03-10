from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , JsonResponse
from accounts.models import User

# Create your views here.
@login_required
def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request , name):
    username = request.user.username
    room_details = Room.objects.get(name=name)
    return render(request , 'room/room.html' , {
        'username' : username ,
        'name' : name ,
        'room_details' : room_details
    })

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value= message , user = username , room = room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')

def getMessages(request , name):
    room_details = Room.objects.get(name=name)
    messages = Message.objects.filter(room = room_details.id).order_by('date')
    return JsonResponse({"messages" :list(messages.values())})
