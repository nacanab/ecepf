from django.urls import path
from .views import *

urlpatterns=[
    path('chat/' , chat , name ="chat"),
    path('conversation/<int:user_id>' , start_conversation , name ="conversation"),
    path('chatroom/<int:room_id>/', room , name ="chatroom"),
    path('send', send , name ="send"),
    path('getchatMessages/<int:room_id>/', getMessages , name ="getchatMessages")
]