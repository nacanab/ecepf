# forms.py
from django import forms

class SerialNumberForm(forms.Form):
    serial_number = forms.CharField(
        label="Numéro de série",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de série'})
    )