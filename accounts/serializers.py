from rest_framework import serializers
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all_'
class StudentSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), required=False)

    class Meta:
        model = User
        fields = [
            'id','first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'is_student', 'program'
        ]
        extra_kwargs = {
            'is_student': {'default': True},  # Forcer is_student à True
        }

    def create(self, validated_data):
        validated_data['is_student'] = True

        # Générer un nom d'utilisateur et un mot de passe aléatoires
        username = validated_data['email']
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            is_student=True
        )
        user.set_password(password)
        user.save()

        # Créer un étudiant
        # student = Student.objects.create(
        #     student=user,
        #     program=validated_data.get('program')
        # )

        # Envoyer un email avec les identifiants
        subject = 'Vos identifiants de connexion'
        message = f"""
            Bonjour {user.first_name} {user.last_name},
            Votre compte a été créé avec succès.
            Identifiant : {user.username}
            Mot de passe : {password}
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user



class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'is_lecturer'
        ]
        extra_kwargs = {
            'is_lecturer': {'default': True},  # Forcer is_lecturer à True
        }

    def create(self, validated_data):
        validated_data['is_lecturer'] = True

        # Générer un nom d'utilisateur et un mot de passe aléatoires
        username = validated_data['email']
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            is_lecturer=True
        )
        user.set_password(password)
        user.save()
        # Envoyer un email avec les identifiants
        subject = 'Vos identifiants de connexion'
        message = f"""
            Bonjour {user.first_name},
            Votre compte a été créé avec succès.
            Identifiant : {user.username}
            Mot de passe : {password}
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user
class DepartmentHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DepartmentHead
        fields = '_all_'

class UserSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSession
        fields = '_all_'

class StudentLogsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentLogs
        fields = '_all_'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '_all_'
        
        
        
###################PROFILE SERIALIZER####################
from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    ville = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    numero_de_telephone = serializers.CharField(source='phone')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'ville', 'email', 'numero_de_telephone']