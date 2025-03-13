from django.urls import path
from .api_views import (
    ExamenListView,
    ExamenDetailView,
    TakeExamenView,
    ResultatListView,
    ResultatDetailView
)

urlpatterns = [
    path('exams/', ExamenListView.as_view(), name='api-exam-list'),
    path('exams/<slug:slug>/', ExamenDetailView.as_view(), name='api-exam-detail'),
    path('exams/<slug:slug>/submit/', TakeExamenView.as_view(), name='api-exam-submit'),
    path('results/', ResultatListView.as_view(), name='api-result-list'),
    path('results/<slug:slug>/', ResultatDetailView.as_view(), name='api-result-detail'),
]