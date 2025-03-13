from django.urls import path
from .views_api import (
    RoomListAPIView,
    RoomDetailAPIView,
    MessageListAPIView,
)

urlpatterns = [
    # Endpoints pour les salles
    path('rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('rooms/<str:name>/', RoomDetailAPIView.as_view(), name='room-detail'),

    # Endpoints pour les messages
    path('rooms/<str:room_name>/messages/', MessageListAPIView.as_view(), name='message-list'),
]