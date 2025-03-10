from django import forms
from .models import Examen, QuestionExamen, ReponseExamen
from course.models import Course

class ExamenForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisez le type HTML5 'date'
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),  # Récupère tous les cours disponibles
        widget=forms.CheckboxSelectMultiple,  # Permet la sélection multiple
        label="Cours associés",  # Libellé du champ
    )

    class Meta:
        model = Examen
        fields = ["courses", "title", "description", "date", "duration", "max_score", "pass_mark", "file"]

class QuestionExamenForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),  # Récupère tous les cours disponibles
        label="Cours associé",  # Libellé du champ
    )

    class Meta:
        model = QuestionExamen
        fields = ["course", "content", "question_type", "score"]

class ExamenActivationForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].label = "Activer l'examen"
        self.fields['is_active'].widget = forms.CheckboxInput()

class ReponseExamenForm(forms.ModelForm):
    class Meta:
        model = ReponseExamen
        fields = ["content", "is_correct"]

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if question:
            if question.question_type == "multiple_choice":
                # Pour les questions à choix multiples
                reponses = question.reponses.all()
                self.fields['reponse'] = forms.ChoiceField(
                    choices=[(r.id, r.content) for r in reponses],
                    widget=forms.RadioSelect,
                    label="Choisissez une réponse"
                )
            elif question.question_type == "true_false":
                # Pour les questions vrai/faux
                self.fields['reponse'] = forms.ChoiceField(
                    choices=[(True, "Vrai"), (False, "Faux")],
                    widget=forms.RadioSelect,
                    label="Vrai ou Faux ?"
                )
            elif question.question_type == "short_answer":
                # Pour les questions à réponse courte
                self.fields['reponse'] = forms.CharField(
                    widget=forms.TextInput,
                    label="Entrez votre réponse"
                )

    def clean(self):
        cleaned_data = super().clean()
        question = self.instance.question if hasattr(self, 'instance') else None

        if question and question.question_type == "short_answer":
            reponse = cleaned_data.get('reponse')
            if not reponse or reponse.strip() == "":
                raise forms.ValidationError("Veuillez entrer une réponse.")
        
        return cleaned_data