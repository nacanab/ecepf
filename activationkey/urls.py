# urls.py
from django.urls import path
from .views import activation_key_view, generate_activation_key_view

urlpatterns = [
    path('generate-activation-key/', generate_activation_key_view, name='generate_activation_key'),
    path('activation-key/<str:activation_key>/<str:expires_at>/', activation_key_view, name='activation_key'),
]