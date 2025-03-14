from rest_framework import serializers
from course.models import Course, CourseAllocation, Upload, UploadVideo, Comment
from accounts.models import User
from result.models import TakenCourse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'slug',
            'title',
            'title_en',
            'code',
            'credit',
            'summary',
            'semester',
            'is_elective',
        ]
        read_only_fields = ['slug']

class CourseAllocationSerializer(serializers.ModelSerializer):
    lecturer = UserSerializer()
    courses = CourseSerializer(many=True)
    
    class Meta:
        model = CourseAllocation
        fields = '__all__'
class UploadSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Upload
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer()
        return super(UploadSerializer, self).to_representation(instance)

class UploadVideoSerializer(serializers.ModelSerializer):
    # Utiliser ce champ pour la validation des données entrantes
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    # Ajouter un champ séparé pour représenter le cours
    course_detail = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = UploadVideo
        fields = ['id', 'video', 'title', 'summary', 'course', 'course_detail']
        # Ajoutez d'autres champs nécessaires
        
    
    # Nous n'avons plus besoin de to_representation car nous utilisons course_detail
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    
    class Meta:
        model = Comment
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super(CommentSerializer, self).to_representation(instance)
class TakenCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenCourse
        fields = '__all__'