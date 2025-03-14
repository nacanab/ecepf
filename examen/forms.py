from django import forms
from .models import Epreuve, Examen, QuestionExamen, ReponseExamen, ResultatExamen
from course.models import Course

class ExamenForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utilisez le type HTML5 'date'
    )


    class Meta:
        model = Examen
        fields = ["title", "description", "date", "pass_mark", ]

class EpreuveForm(forms.ModelForm):
    class Meta:
        model = Epreuve
        fields = ["course", "duration", "max_score","file"]
        
class QuestionExamenForm(forms.ModelForm):
    class Meta:
        model = QuestionExamen
        fields = ["epreuve", "content", "question_type", "score"]


class EpreuveActivationForm(forms.ModelForm):
    class Meta:
        model = Epreuve
        fields = ['is_active']


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
                
class ResultatExamenForm(forms.ModelForm):
    class Meta:
        model = ResultatExamen
        fields = ['reponse_text']

    def __init__(self, *args, **kwargs):
        epreuve = kwargs.pop('epreuve', None)
        super(ResultatExamenForm, self).__init__(*args, **kwargs)

        if not epreuve or not epreuve.file:  # Désactive le champ si pas de fichier
            self.fields['reponse_text'].widget = forms.HiddenInput()