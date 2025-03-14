from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NewsAndEventsViewSet, SessionViewSet, SemesterViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register(r'news-and-events', NewsAndEventsViewSet, basename='news-and-events')
router.register(r'sessions', SessionViewSet, basename='sessions')
router.register(r'semesters', SemesterViewSet, basename='semesters')
router.register(r'activity-logs', ActivityLogViewSet, basename='activity-logs')

urlpatterns = [
    path('', include(router.urls)),
]