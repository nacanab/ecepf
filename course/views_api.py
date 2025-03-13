from rest_framework import viewsets, permissions, parsers
from course.models import Course, CourseAllocation, Upload, UploadVideo, Comment
from rest_framework.permissions import AllowAny
from result.models import TakenCourse
from .serializers import *

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    search_fields = ['title', 'code', 'summary']

class CourseAllocationViewSet(viewsets.ModelViewSet):
    queryset = CourseAllocation.objects.all()
    serializer_class = CourseAllocationSerializer
    permission_classes = [AllowAny]

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]

class UploadVideoViewSet(viewsets.ModelViewSet):
    queryset = UploadVideo.objects.all()
    serializer_class = UploadVideoSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class TakenCourseViewSet(viewsets.ModelViewSet):
    serializer_class = TakenCourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        return TakenCourse.objects.filter(student__student=user)