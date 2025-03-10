from django.shortcuts import render,get_object_or_404,redirect

from badges.froms import AttributionBadgeForm
from .models import Badge,AttributionBadge
from accounts.models import Lecturer, Student
from accounts.decorators import lecturer_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required
def badge_list(request):
    badges=AttributionBadge.objects.filter(student_id=7)
    render(request,"accounts/profile.html",{'badges':badges})

@login_required
@lecturer_required
def attribuer_badge(request):
    lecturer = Lecturer.objects.get(user=request.user)
    if request.method == 'POST':
        form = AttributionBadgeForm(request.POST,lecturer=lecturer)
        if form.is_valid():
            form.save()
            return redirect('lecturer_student_list',lecturer.user.id)  # Redirige vers la liste des élèves
    else:
        form = AttributionBadgeForm(lecturer=lecturer)
    return render(request, 'badges/attribuer_badge.html', {'form': form})

@login_required
@lecturer_required
def revoquer_badge(request,student_id,attribution_id):
    attribution=get_object_or_404(AttributionBadge,id=attribution_id)
    attribution.delete()
    messages.success(request,"badge suprrimé avec succès")
    return redirect("profil_etudiant",student_id)


