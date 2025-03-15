from rest_framework import serializers
from .models import User, Student, Lecturer, Parent, DepartmentHead, UserSession, StudentLogs, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Student, Lecturer, Parent, Program
import string
import random
from django.core.mail import send_mail
from django.conf import settings
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
        
        lecturer = Lecturer.objects.create(lecturer=user)
        lecturer.save()
        
        return user


        
        
###################Parent SERIALIZER####################
# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Parent, Student, RELATION_SHIP

#User = get_user_model()

# class ParentSerializer(serializers.ModelSerializer):
#     # Redéfinir ces champs comme read_only pour la récupération GET
#     username = serializers.SerializerMethodField()
#     email = serializers.SerializerMethodField()
#     first_name = serializers.SerializerMethodField()
#     last_name = serializers.SerializerMethodField()
    
#     # Garder ces champs pour les opérations d'écriture (POST)
#     password = serializers.CharField(write_only=True, required=True)
#     password_confirmation = serializers.CharField(write_only=True, required=True)
#     address = serializers.CharField(write_only=True, required=True)
#     phone_number = serializers.CharField(write_only=True, required=True)
    
#     # Champs pour l'étudiant
#     student_username = serializers.CharField(write_only=True, required=True)
#     student_password = serializers.CharField(write_only=True, required=True)
    
#     # Ce champ existe dans Parent
#     relation_ship = serializers.ChoiceField(choices=RELATION_SHIP, required=True)
    
#     class Meta:
#         model = Parent
#         fields = [
#             'username', 'email', 'password', 'password_confirmation',
#             'address', 'phone_number', 'first_name', 'last_name',
#             'student_username', 'student_password', 'relation_ship'
#         ]
    
#     # Méthodes pour récupérer les données du User lié
#     def get_username(self, obj):
#         return obj.user.username if obj.user else None
    
#     def get_email(self, obj):
#         return obj.user.email if obj.user else None
    
#     def get_first_name(self, obj):
#         return obj.user.first_name if obj.user else None
    
#     def get_last_name(self, obj):
#         return obj.user.last_name if obj.user else None
    
#     def validate(self, data):
#         # Vérifier que les mots de passe correspondent (seulement pour créations POST)
#         if 'password' in data and 'password_confirmation' in data:
#             if data['password'] != data['password_confirmation']:
#                 raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
#         # Vérifier si l'username existe déjà (seulement pour créations POST)
#         if 'username' in data and User.objects.filter(username=data['username']).exists():
#             raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà utilisé."})
        
#         # Vérifier si l'email existe déjà (seulement pour créations POST)
#         if 'email' in data and User.objects.filter(email=data['email']).exists():
#             raise serializers.ValidationError({"email": "Cette adresse email est déjà utilisée."})
            
#         return data
    
#     def create(self, validated_data):
#         # Extraire les données pour User
#         username = validated_data.pop('username', None)
#         email = validated_data.pop('email', None)
#         password = validated_data.pop('password', None)
#         validated_data.pop('password_confirmation', None)
        
#         address = validated_data.pop('address', None)
#         phone_number = validated_data.pop('phone_number', None)
#         first_name = validated_data.pop('first_name', None)
#         last_name = validated_data.pop('last_name', None)
        
#         # Extraire les données pour l'étudiant
#         student_username = validated_data.pop('student_username', None)
#         student_password = validated_data.pop('student_password', None)
#         relation_ship = validated_data.pop('relation_ship', None)
        
#         # Créer l'utilisateur parent
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone_number,
#             address=address,
#             is_parent=True
#         )
        
#         # Vérifier si l'étudiant existe déjà, sinon le créer
#         try:
#             student_user = User.objects.get(username=student_username)
#             try:
#                 student = Student.objects.get(student=student_user)
#             except Student.DoesNotExist:
#                 # Si l'utilisateur existe mais pas l'étudiant
#                 student = Student.objects.create(student=student_user)
#         except User.DoesNotExist:
#             # Créer l'utilisateur étudiant
#             student_user = User.objects.create_user(
#                 username=student_username,
#                 password=student_password,
#                 is_student=True
#             )
#             # Créer l'étudiant
#             student = Student.objects.create(student=student_user)
        
#         # Créer le parent
#         parent = Parent.objects.create(
#             user=user,
#             student=student,
#             relation_ship=relation_ship
#         )
        
#         return parent
    


class ParentSerializer(serializers.ModelSerializer):
    # Définition des champs provenant de User avec SerializerMethodField pour GET
    username = serializers.SerializerMethodField(read_only=True)
    # Pour l'entrée POST, définir des champs séparés
    username_input = serializers.CharField(write_only=True, required=True, source='username')
    
    email = serializers.SerializerMethodField(read_only=True)
    email_input = serializers.EmailField(write_only=True, required=True, source='email')
    
    first_name = serializers.SerializerMethodField(read_only=True)
    first_name_input = serializers.CharField(write_only=True, required=True, source='first_name')
    
    last_name = serializers.SerializerMethodField(read_only=True)
    last_name_input = serializers.CharField(write_only=True, required=True, source='last_name')
    
    address = serializers.SerializerMethodField(read_only=True)
    address_input = serializers.CharField(write_only=True, required=True, source='address')
    
    phone_number = serializers.SerializerMethodField(read_only=True)
    phone_number_input = serializers.CharField(write_only=True, required=True, source='phone_number')
    
    # Champs pour l'écriture uniquement (POST)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    # Champs pour l'étudiant (POST)
    student_username = serializers.CharField(write_only=True, required=True)
    student_password = serializers.CharField(write_only=True, required=True)
    
    # Ce champ existe dans Parent
    relation_ship = serializers.ChoiceField(choices=RELATION_SHIP, required=True)
    
    class Meta:
        model = Parent
        fields = [
            'username', 'username_input',
            'email', 'email_input', 
            'password', 'password_confirmation',
            'address', 'address_input', 
            'phone_number', 'phone_number_input',
            'first_name', 'first_name_input',
            'last_name', 'last_name_input',
            'student_username', 'student_password',
            'relation_ship'
        ]
    
    # Méthodes pour GET
    def get_username(self, obj):
        return obj.user.username if hasattr(obj, 'user') and obj.user else None
    
    def get_email(self, obj):
        return obj.user.email if hasattr(obj, 'user') and obj.user else None
    
    def get_first_name(self, obj):
        return obj.user.first_name if hasattr(obj, 'user') and obj.user else None
    
    def get_last_name(self, obj):
        return obj.user.last_name if hasattr(obj, 'user') and obj.user else None
    
    def get_address(self, obj):
        return obj.user.address if hasattr(obj, 'user') and obj.user else None
    
    def get_phone_number(self, obj):
        return obj.user.phone if hasattr(obj, 'user') and obj.user else None
    
    def validate(self, data):
        # Extraire les données du dictionnaire source
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        
        # Vérifier que les mots de passe correspondent
        if password != password_confirmation:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        # Vérifier si l'username existe déjà
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà utilisé."})
        
        # Vérifier si l'email existe déjà
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Cette adresse email est déjà utilisée."})
            
        return data
    
    def create(self, validated_data):
        # Extraire les données pour User
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirmation', None)  # On n'a plus besoin de ce champ
        
        address = validated_data.pop('address', None)
        phone_number = validated_data.pop('phone_number', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        
        # Extraire les données pour l'étudiant
        student_username = validated_data.pop('student_username', None)
        student_password = validated_data.pop('student_password', None)
        relation_ship = validated_data.pop('relation_ship', None)
        
        # Créer l'utilisateur parent
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone_number,
            address=address,
            is_parent=True
        )
        
        # Vérifier si l'étudiant existe déjà, sinon le créer
        try:
            student_user = User.objects.get(username=student_username)
            try:
                student = Student.objects.get(student=student_user)
            except Student.DoesNotExist:
                # Si l'utilisateur existe mais pas l'étudiant
                student = Student.objects.create(student=student_user)
        except User.DoesNotExist:
            # Créer l'utilisateur étudiant
            student_user = User.objects.create_user(
                username=student_username,
                password=student_password,
                is_student=True
            )
            # Créer l'étudiant
            student = Student.objects.create(student=student_user)
        
        # Créer le parent
        parent = Parent.objects.create(
            user=user,
            student=student,
            relation_ship=relation_ship
        )
        
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


        
###################PROFILE SERIALIZER####################
from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    ville = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    numero_de_telephone = serializers.CharField(source='phone')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'ville', 'email', 'numero_de_telephone','is_student','is_lecturer']
        
        
        
        
###################Forgoted password SERIALIZER####################
# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        # Vérifier si l'email existe et si l'utilisateur est actif
        if not User.objects.filter(email__iexact=value, is_active=True).exists():
            raise serializers.ValidationError(_("Aucun utilisateur actif n'est enregistré avec cette adresse email."))
        return value
    
    def save(self):
        request = self.context.get('request')
        
        # Utiliser le formulaire de réinitialisation de mot de passe de Django
        form = PasswordResetForm(data=self.validated_data)
        if form.is_valid():
            # Envoyer l'email de réinitialisation
            form.save(
                request=request,
                from_email=None,  # Utiliser l'email par défaut configuré dans settings
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt'
            )
        return self.validated_data