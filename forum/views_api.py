from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer

class RoomListAPIView(generics.ListAPIView):
    """
    API pour lister toutes les salles.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Autorise tout le monde

class RoomDetailAPIView(generics.RetrieveAPIView):
    """
    API pour récupérer les détails d'une salle.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'name'  # Recherche par le nom de la salle
    permission_classes = [AllowAny]  # Autorise tout le monde

class MessageListAPIView(generics.ListCreateAPIView):
    """
    API pour lister et envoyer des messages dans une salle.
    """
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]  # Authentification requise

    def get_queryset(self):
        # Récupérer les messages d'une salle spécifique
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room=room_name).order_by('date')

    def perform_create(self, serializer):
        # Enregistrer le message avec l'utilisateur et la salle
        room_name = self.kwargs['room_name']
        serializer.save(
            room=room_name,
            user=self.request.user.username
        )