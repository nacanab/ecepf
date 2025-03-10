from django.urls import path
from forum import views

urlpatterns=[
    path('listeroom/' , views.list_rooms , name ="rooms"),
    path('<str:name>/', views.room , name ="room"),
    path('send', views.send , name ="send"),
    path('getMessages/<str:name>/', views.getMessages , name ="getMessages")
]