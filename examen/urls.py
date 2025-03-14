from django.urls import path
from . import views

urlpatterns = [
    path("", views.examen_list, name="examen_list"),
    path("create/", views.examen_create, name="examen_create"),
    path("<slug:slug>/", views.examen_detail, name="examen_detail"),
    path("<slug:slug>/update/", views.examen_update, name="examen_update"),
    path("<slug:slug>/delete/", views.examen_delete, name="examen_delete"),
    path("<int:epreuve_id>/question/create/", views.question_create, name="question_create"),
    path("question/<int:question_id>/update/", views.question_update, name="question_update"),
    path("question/<int:question_id>/delete/", views.question_delete, name="question_delete"),
    path("question/<int:question_id>/reponse/create/", views.reponse_create, name="reponse_create"),
    path("reponse/<int:reponse_id>/update/", views.reponse_update, name="reponse_update"),
    path("reponse/<int:reponse_id>/delete/", views.reponse_delete, name="reponse_delete"),
    path("<int:epreuve_id>/take/", views.take_examen, name="take_examen"),
    path("<int:epreuve_id>/results/", views.epreuve_results, name="epreuve_results"),
    # Soumission des examens par les étudiants

    # Correction des examens par l'enseignant (affichage du tableau)
     path('examen/<slug:examen_slug>/creer-epreuve/', views.creer_epreuve, name='epreuve_create'),
     path("examen/<int:epreuve_id>/", views.epreuve_detail, name="epreuve_detail"),
     path('examen/<int:epreuve_id>/modifier-epreuve/', views.epreuve_update, name='epreuve_update'),
     path('examen/<int:epreuve_id>/supprimer-epreuve/', views.epreuve_delete, name='epreuve_delete'),
    path('examen/<int:epreuve_id>/correction/', views.correction_examens, name='correction_examens'),
    path('epreuve/<int:epreuve_id>/activate/', views.epreuve_activation, name='epreuve_activation'),
    path('examen/<slug:examen_slug>/notes/', views.notes_et_moyennes_examen, name='notes_et_moyennes_examen'),
]