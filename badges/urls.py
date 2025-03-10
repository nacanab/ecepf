from django.urls import path
from . import views

urlpatterns = [
    path('attribuer_badge/', views.attribuer_badge, name='attribuer_badge'),
    path('badges_list/', views.badge_list, name='badges_eleve'),
    path('revoquer_badge/<int:student_id>/<int:attribution_id>/', views.revoquer_badge, name='delete_badge'),
]