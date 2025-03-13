from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r'courses', views_api.CourseViewSet)
router.register(r'allocations', views_api.CourseAllocationViewSet)
router.register(r'uploads', views_api.UploadViewSet)
router.register(r'videos', views_api.UploadVideoViewSet)
router.register(r'comments', views_api.CommentViewSet)
router.register(r'registrations', views_api.TakenCourseViewSet, basename='registrations')

urlpatterns = [
    path('', include(router.urls)),
]