from django.urls import path
from . import views

urlpatterns = [
  path('dictionnary', views.word, name='word'),
]