from rest_framework import viewsets, permissions, parsers, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    @action(detail=False, methods=['post'])
    def upload_file(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadVideoViewSet(viewsets.ModelViewSet):
    queryset = UploadVideo.objects.all()
    serializer_class = UploadVideoSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    @action(detail=False, methods=['post'])
    def upload_video(self, request):
        serializer = UploadVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class TakenCourseViewSet(viewsets.ModelViewSet):
    serializer_class = TakenCourseSerializer
    permission_classes = [AllowAny]
    queryset = TakenCourse.objects.all()
    
    def get_queryset(self):
        # Si l'utilisateur est authentifié, filtrez par utilisateur
        if self.request.user.is_authenticated:
            return TakenCourse.objects.filter(student__student=self.request.user)
        # Sinon, retournez tous les cours pris
        return TakenCourse.objects.all()