from django.urls import path
from . import views

urlpatterns = [
    path('chatbot', views.ChatbotGenerateAnswerView.as_view(), name='chatbot'),
    path('api/chat/', views.ChatbotGenerateAnswerView.as_view(), name='chat_api'),
]