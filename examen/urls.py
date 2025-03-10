from django.urls import path
from . import views

urlpatterns = [
    path("", views.examen_list, name="examen_list"),
    path("create/", views.examen_create, name="examen_create"),
    path("<slug:slug>/", views.examen_detail, name="examen_detail"),
    path("<slug:slug>/update/", views.examen_update, name="examen_update"),
    path("<slug:slug>/delete/", views.examen_delete, name="examen_delete"),
    path("<slug:slug>/question/create/", views.question_create, name="question_create"),
    path("question/<int:question_id>/update/", views.question_update, name="question_update"),
    path("question/<int:question_id>/delete/", views.question_delete, name="question_delete"),
    path("question/<int:question_id>/reponse/create/", views.reponse_create, name="reponse_create"),
    path("reponse/<int:reponse_id>/update/", views.reponse_update, name="reponse_update"),
    path("reponse/<int:reponse_id>/delete/", views.reponse_delete, name="reponse_delete"),
    path("<slug:slug>/take/", views.take_examen, name="take_examen"),
    path("<slug:slug>/results/", views.examen_results, name="examen_results"),
    path('examen/activation/<int:examen_id>/', views.examen_activation, name='examen_activation'),
]