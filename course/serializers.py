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
    course = CourseSerializer()
    
    class Meta:
        model = Upload
        fields = '__all__'

class UploadVideoSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    
    class Meta:
        model = UploadVideo
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'

class TakenCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenCourse
        fields = '__all__'