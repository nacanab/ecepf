from rest_framework import generics, status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs
from .serializers import UserSerializer, StudentSerializer, LecturerSerializer, ParentSerializer, DepartmentHeadSerializer, UserSessionSerializer, StudentLogsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny  # Ajoutez cette ligne pour importer AllowAny
from rest_framework.authtoken.models import Token


class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Autoriser l'accès sans authentification

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_400_BAD_REQUEST)
        


from rest_framework.permissions import IsAuthenticated, AllowAny  # Seuls les utilisateurs authentifiés peuvent se déconnecter

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs authentifiés peuvent accéder à cette vue

    def post(self, request, *args, **kwargs):
        try:
            # Supprimer le token de l'utilisateur
            request.user.auth_token.delete()
            return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout, authenticate
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs
from .serializers import (
    UserSerializer, StudentSerializer, LecturerSerializer, ParentSerializer,
    DepartmentHeadSerializer, UserSessionSerializer, StudentLogsSerializer, ProfileSerializer
)

# Vues pour User
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Vues pour Student
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

# Vues pour Lecturer
class LecturerListCreateView(generics.ListCreateAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

class LecturerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

# Vues pour Parent
class ParentListCreateView(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]

class ParentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]

# Vues pour DepartmentHead
class DepartmentHeadListCreateView(generics.ListCreateAPIView):
    queryset = DepartmentHead.objects.all()
    serializer_class = DepartmentHeadSerializer
    permission_classes = [IsAuthenticated]

class DepartmentHeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DepartmentHead.objects.all()
    serializer_class = DepartmentHeadSerializer
    permission_classes = [IsAuthenticated]

# Vues pour UserSession
class UserSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]

class UserSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]

# Vues pour StudentLogs
class StudentLogsListCreateView(generics.ListCreateAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [IsAuthenticated]

class StudentLogsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [IsAuthenticated]

# Vues supplémentaires
class StudentCreateAPIView(APIView):
    """API pour créer un nouvel étudiant avec génération automatique des identifiants."""
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': f'Compte étudiant créé avec succès pour {user.get_full_name()}',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins

class LecturerCreateAPIView(APIView):
    """API pour créer un nouveau professeur avec génération automatique des identifiants."""
    permission_classes = [AllowAny]  # Ajustez selon vos besoins de sécurité

    def post(self, request, *args, **kwargs):
        serializer = LecturerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': f'Compte enseignant créé avec succès pour {user.get_full_name()}',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LecturerListView(generics.ListAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny]  # Ajustez selon vos besoins

class LecturerDetailView(generics.RetrieveAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = Lecturer    
    



# views_api.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Parent
from .serializers import ParentSerializer

class ParentCreateAPIView(APIView):
    """
    API pour créer un nouveau parent.
    """
    permission_classes = [AllowAny]  # Changer selon vos besoins de sécurité

    def post(self, request, *args, **kwargs):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                parent = serializer.save()
                return Response({
                    'status': 'success',
                    'message': f'Compte parent créé avec succès pour {parent.user.get_full_name()}',
                    'user_id': parent.user.id,
                    'email': parent.user.email,
                    'student_id': parent.student.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentListView(generics.ListAPIView):
    """
    Liste de tous les parents.
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]

class ParentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, mise à jour et suppression d'un parent.
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]



#Pour le profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        # Si un ID est fourni, récupérer le profil spécifique
        if pk:
            try:
                user = User.objects.get(pk=pk)
                serializer = ProfileSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(
                    {"error": "Utilisateur non trouvé"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        # Sinon, récupérer tous les profils (si nécessaire)
        else:
            users = User.objects.all()
            serializer = ProfileSerializer(users, many=True)
            return Response(serializer.data)


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Utilisez l'utilisateur de la requête (authentifié)
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)