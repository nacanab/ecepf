import logging
from rest_framework import generics, status, views
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs
from .serializers import UserSerializer, StudentSerializer, LecturerSerializer, ParentSerializer, DepartmentHeadSerializer, UserSessionSerializer, StudentLogsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny  # Ajoutez cette ligne pour importer AllowAny
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

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
    permission_classes = [AllowAny]  # Seuls les utilisateurs authentifiés peuvent accéder à cette vue

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
    permission_classes = [AllowAny]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

class DepartmentHeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DepartmentHead.objects.all()
    serializer_class = DepartmentHeadSerializer
    permission_classes = [AllowAny]

# Vues pour UserSession
class UserSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [AllowAny]

class UserSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [AllowAny]

# Vues pour StudentLogs
class StudentLogsListCreateView(generics.ListCreateAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [AllowAny]

class StudentLogsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]  # Ajustez selon vos besoins
    



class ParentListView(generics.ListAPIView):
    """
    API endpoint to list all parents
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]  # Adjust based on your security requirements


class ParentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update or delete a parent
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]  # Adjust based on your security requirements




# views_api.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ParentSerializer

class ParentCreateAPIView(APIView):
    """
    API pour créer un nouveau parent.
    """
    permission_classes = [AllowAny]  # Changer selon vos besoins de sécurité
    
    def post(self, request, *args, **kwargs):
        # Débogage - afficher les données reçues
        print(f"Données reçues: {request.data}")
        
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                parent = serializer.save()
                return Response({
                    'status': 'success',
                    'message': f'Compte parent créé avec succès pour {parent.user.get_full_name}',
                    'user_id': parent.user.id,
                    'email': parent.user.email,
                    'student_id': parent.student.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Erreur lors de la création du parent: {str(e)}")
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        print(f"Erreurs de validation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
# views_api.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordResetSerializer

# Dans votre views_api.py
class PasswordResetView(APIView):
    def post(self, request):
        # Ajouter des logs pour déboguer
        print(f"Données reçues: {request.data}")
        
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"detail": "Un email de réinitialisation a été envoyé si un compte avec cette adresse existe."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                # Logger l'erreur pour le débogage
                print(f"Erreur lors de l'envoi de l'email: {str(e)}")
                return Response(
                    {"detail": "Erreur lors de l'envoi de l'email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)