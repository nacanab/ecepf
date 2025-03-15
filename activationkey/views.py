# views.py
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from activationkey.models import ActivatedDevice
from .forms import SerialNumberForm
from .utils import generate_activation_key


def generate_activation_key_view(request):
    if request.method == 'POST':
        form = SerialNumberForm(request.POST)
        if form.is_valid():
            serial_number = form.cleaned_data['serial_number']
            
            # Vérifiez si une clé existe déjà pour ce numéro de série
            if ActivatedDevice.objects.filter(serial_number=serial_number).exists():
                messages.error(request, 'Une clé existe déjà pour ce numéro de série.')
            else:
                # Générer la clé d'activation
                activation_key = generate_activation_key(serial_number)
                
                # Définir la date d'expiration (par exemple, 30 jours après la création)
                expires_at = timezone.now() + timedelta(days=30)
                
                # Enregistrer la clé dans la base de données
                ActivatedDevice.objects.create(
                    serial_number=serial_number,
                    activation_key=activation_key,
                    expires_at=expires_at,
                )
                
                # Afficher la clé générée et sa date d'expiration à l'utilisateur
                messages.success(request, f'Clé d\'activation générée : {activation_key}. Expire le {expires_at.strftime("%Y-%m-%d %H:%M:%S")}')
            
            return redirect('activation_key',activation_key=activation_key,expires_at=expires_at.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        form = SerialNumberForm()
    
    return render(request, 'activationkey/generate.html', {'form': form})


@login_required
def activation_key_view(request, activation_key,expires_at):
    context = {
        'activation_key': activation_key,
        'expires_at': expires_at,
    }
    return render(request, 'activationkey/activation_key.html', context)