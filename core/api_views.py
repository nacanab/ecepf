from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from .models import NewsAndEvents, Session, Semester, ActivityLog
from .serializers import NewsAndEventsSerializer, SessionSerializer, SemesterSerializer, ActivityLogSerializer

# News & Events
class NewsAndEventsViewSet(viewsets.ModelViewSet):
    queryset = NewsAndEvents.objects.all().order_by('-updated_date')
    serializer_class = NewsAndEventsSerializer
    permission_classes = [AllowAny]

# Session
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all().order_by('-is_current_session', '-session')
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

# Semester
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all().order_by('-is_current_semester', '-semester')
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]

# Activity Log
class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    permission_classes = [AllowAny]