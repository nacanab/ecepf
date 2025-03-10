from django import forms
from .models import AttributionBadge, Badge
from accounts.models import Student

class AttributionBadgeForm(forms.ModelForm):
    class Meta:
        model = AttributionBadge
        fields = ['student', 'badge']

    def __init__(self, *args, lecturer=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lecturer:
            # Filtrer les élèves pour n'afficher que ceux de l'enseignant connecté
            self.fields['student'].queryset = lecturer.students.all()
        else:
            self.fields['student'].queryset = Student.objects.none()  # Aucun élève si aucun enseignant n'est spécifié
        self.fields['badge'].queryset = Badge.objects.all()  # Affiche tous les badges