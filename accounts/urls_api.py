from django.urls import path
from .views_api import (
    UserListCreateView, UserRetrieveUpdateDestroyView,
    StudentListCreateView, StudentRetrieveUpdateDestroyView,
    LecturerListCreateView, LecturerRetrieveUpdateDestroyView,
    ParentListCreateView, ParentRetrieveUpdateDestroyView,
    DepartmentHeadListCreateView, DepartmentHeadRetrieveUpdateDestroyView,
    UserSessionListCreateView, UserSessionRetrieveUpdateDestroyView,
    StudentLogsListCreateView, StudentLogsRetrieveUpdateDestroyView,
    LoginAPIView, LogoutAPIView, LecturerCreateAPIView, ProfileAPIView,MyProfileAPIView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-retrieve-update-destroy'),
    path('lecturers/', LecturerListCreateView.as_view(), name='lecturer-list-create'),
    path('lecturers/<int:pk>/', LecturerRetrieveUpdateDestroyView.as_view(), name='lecturer-retrieve-update-destroy'),
    path('parents/', ParentListCreateView.as_view(), name='parent-list-create'),
    path('parents/<int:pk>/', ParentRetrieveUpdateDestroyView.as_view(), name='parent-retrieve-update-destroy'),
    path('department-heads/', DepartmentHeadListCreateView.as_view(), name='department-head-list-create'),
    path('department-heads/<int:pk>/', DepartmentHeadRetrieveUpdateDestroyView.as_view(), name='department-head-retrieve-update-destroy'),
    path('user-sessions/', UserSessionListCreateView.as_view(), name='user-session-list-create'),
    path('user-sessions/<int:pk>/', UserSessionRetrieveUpdateDestroyView.as_view(), name='user-session-retrieve-update-destroy'),
    path('student-logs/', StudentLogsListCreateView.as_view(), name='student-logs-list-create'),
    path('student-logs/<int:pk>/', StudentLogsRetrieveUpdateDestroyView.as_view(), name='student-logs-retrieve-update-destroy'),
    
    # Routes API pour le login et le logout
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    #Profile
    path('profile/', ProfileAPIView.as_view(), name='profiles'),
    #path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile_detail_api'),
    
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile-detail'),
    path('my-profile/', MyProfileAPIView.as_view(), name='my-profile'),
    # Route API pour la création de Lecturer
    path('lecturer/create/', LecturerCreateAPIView.as_view(), name='lecturer-create'),
]