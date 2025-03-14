from rest_framework import serializers
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from .models import User, Student, Lecturer, Parent, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Correction de '_all_' à '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class StudentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'gender', 'phone', 
            'address', 'is_student'
        ]
        extra_kwargs = {
            'is_student': {'default': True},
        }

    def create(self, validated_data):
        # Génération d'un nom d'utilisateur et d'un mot de passe aléatoire
        username = validated_data.get('email')
       
        
        # Création de l'utilisateur
        validated_data['is_student'] = True
        user = User.objects.create_user(
            username=username,
           
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            gender=validated_data.get('gender', 'M'),  # Valeur par défaut si non fournie
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            is_student=True
        )
        
        # Création de l'étudiant
        student = Student.objects.create(student=user)
        student.save()
        return user

class LecturerSerializer(serializers.ModelSerializer):
    #department = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), required=False)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'gender', 'phone', 
            'address', 'is_lecturer'
        ]
        extra_kwargs = {
            'is_lecturer': {'default': True},
        }

    def create(self, validated_data):
        # Génération d'un nom d'utilisateur et d'un mot de passe aléatoire
        username = validated_data.get('email')
        
        
        # Création de l'utilisateur
        validated_data['is_lecturer'] = True
        user = User.objects.create_user(
            username=username,
            
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            gender=validated_data.get('gender', 'M'),  # Valeur par défaut si non fournie
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            is_lecturer=True
        )
        
        lecturer = Student.objects.create(student=user)
        lecturer.save()
        
        return user

from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from .models import User, Parent, Student

class ParentSerializer(serializers.ModelSerializer):
    user = serializers.JSONField(write_only=True, required=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    student_password = serializers.CharField(write_only=True)
    user_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'user', 'student', 'relation_ship', 'student_password', 'user_info']
        read_only_fields = ['id']

    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'full_name': obj.user.get_full_name()
        }

    def validate(self, data):
        # Vérifier que le mot de passe de l'étudiant est correct
        student = data.get('student')
        student_password = data.get('student_password')
        
        # Vérifie si student a un attribut 'student'
        student_user = getattr(student, 'student', student)
        
        if not hasattr(student_user, 'check_password') or not student_user.check_password(student_password):
            raise serializers.ValidationError("Le mot de passe de l'étudiant est incorrect.")
        
        return data

    def create(self, validated_data):
        # Extraction des données
        student = validated_data.pop('student')
        validated_data.pop('student_password')  # On n'a plus besoin de ce champ
        user_data = validated_data.pop('user')
        
        # Vérification des données requises
        if not user_data.get('email'):
            raise serializers.ValidationError("L'adresse email est requise.")
        
        # Création de l'utilisateur parent
        username = user_data.get('username', f"parent_{student.student.username}")
        password = user_data.get('password', ''.join(random.choices(string.ascii_letters + string.digits, k=8)))
        
        # Vérifier si l'email existe déjà
        if User.objects.filter(email=user_data.get('email')).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
            
        user = User.objects.create_user(
            username=username,
            password=password,
            email=user_data.get('email'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            phone=user_data.get('phone', ''),
            address=user_data.get('address', ''),
            is_parent=True
        )
        
        # Création du parent
        relation_ship = validated_data.get('relation_ship', 'Autre')
        parent = Parent.objects.create(user=user, student=student, relation_ship=relation_ship)
        
        # Envoi d'email
        send_welcome_email(user, password, student)
        
        return parent

def send_welcome_email(user, password, student):
    subject = 'Vos identifiants de connexion'
    message = f"""
        Bonjour {user.get_full_name()},
        Votre compte parent a été créé avec succès.
        Identifiant : {user.username}
        Mot de passe : {password}
        Vous êtes lié(e) à l'étudiant {student.student.get_full_name() if hasattr(student, 'student') else student.get_full_name()}.
        Songez à modifier vos informations de connexion une fois connecté.
        
        Cordialement,
        L'équipe de eCEP
    """
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except Exception as e:
        # Gérer l'erreur ou simplement la logger
        print(f"Erreur lors de l'envoi de l'email: {e}")
        

class DepartmentHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentHead
        fields = '__all__'

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'

class StudentLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLogs
        fields = '__all__'

# Sérialiseur de profil (adapté à partir de votre code)
class ProfileSerializer(serializers.ModelSerializer):
    ville = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    numero_de_telephone = serializers.CharField(source='phone')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'ville', 'email', 'numero_de_telephone']
class DepartmentHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DepartmentHead
        fields = '__all__'

class UserSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSession
        fields = '__all__'

class StudentLogsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentLogs
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        
        
        
###################PROFILE SERIALIZER####################
from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    ville = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    numero_de_telephone = serializers.CharField(source='phone')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'ville', 'email', 'numero_de_telephone']