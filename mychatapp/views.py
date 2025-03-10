from django.shortcuts import render , redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , JsonResponse
from accounts.models import User

# Create your views here.
@login_required
def chat(request):
    current_student = get_object_or_404(Student, student_id=request.user.id)
    friends = User.objects.filter(is_student=True).exclude(id=request.user.id)
    search_query = request.GET.get('search', '')
    
    if search_query:
        friends = friends.filter(friend__username__icontains=search_query)
    
    context = {
        'friends': friends,
        'search_query': search_query,
    }
    return render(request, 'mychatapp/chat.html', context)


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Sauvegarder le fichier et retourner l'URL
        return JsonResponse({'file_url': uploaded_file.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def room(request , room_id):
    username = request.user.username
    room_details = Room.objects.get(id=room_id)
    return render(request , 'mychatapp/room.html' , {
        'username' : username ,
        'room_id' : room_id  ,
        'room_details' : room_details
    })

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value= message , user = username , room = room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')

def getMessages(request , room_id):
    room_details = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room = room_details.id).order_by('date')
    return JsonResponse({"messages" :list(messages.values())})

@login_required
def start_conversation(request, user_id):
    user_2 = get_object_or_404(User, id=user_id)
    user_1 = request.user
    conversation = Room.objects.filter(participants=user_1).filter(participants=user_2).first()
    if not conversation:
        conversation = Room.objects.create()
        conversation.participants.add(user_1,user_2)
    return redirect('chatroom', room_id=conversation.id)