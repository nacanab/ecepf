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
        




class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
    

###partie complete
class LecturerListCreateView(generics.ListCreateAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny]

class LecturerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [AllowAny]
###################

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]




class ParentListCreateView(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]

class ParentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]
    
    
    

class DepartmentHeadListCreateView(generics.ListCreateAPIView):
    queryset = DepartmentHead.objects.all()
    serializer_class = DepartmentHeadSerializer
    permission_classes = [IsAuthenticated]

class DepartmentHeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DepartmentHead.objects.all()
    serializer_class = DepartmentHeadSerializer
    permission_classes = [IsAuthenticated]

class UserSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]

class UserSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    
    
class StudentLogsListCreateView(generics.ListCreateAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [IsAuthenticated]

class StudentLogsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentLogs.objects.all()
    serializer_class = StudentLogsSerializer
    permission_classes = [IsAuthenticated]
 
 
 
class LecturerCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LecturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class StudentCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
#Pour le profile
from rest_framework import generics
from .models import User
from .serializers import ProfileSerializer

class ProfileAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer