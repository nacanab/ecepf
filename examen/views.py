from turtle import title
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from accounts.decorators import admin_required, lecturer_required
from .models import Epreuve, Examen, QuestionExamen, ReponseExamen, ResultatExamen, Soumission
from .forms import EpreuveForm, ExamenForm, QuestionExamenForm, ReponseExamenForm,EpreuveActivationForm, ResultatExamenForm
from django.utils.text import slugify
from accounts.models import Lecturer, Student, UserProfile
from django.db.models import Avg
from config.firebase_utils import send_push_notification

# Liste des examens
@login_required
def examen_list(request):
    examens = Examen.objects.all()
    return render(request, "examen/examen_list.html", {"examens": examens})

# Détails d'un examen
@login_required
def examen_detail(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    return render(request, "examen/examen_detail.html", {"examen": examen})

# Créer un examen
@login_required
def examen_create(request):
    user_profiles = UserProfile.objects.all()
    if request.method == "POST":
        form = ExamenForm(request.POST,request.FILES)
        if form.is_valid():
            examen = form.save(commit=False)
            examen.slug = slugify(examen.title)
            examen.save()
            form.save_m2m()  # Sauvegarder les cours associés
            for profile in user_profiles:
                token = profile.firebase_token
                if token:
                    # Envoyer une notification
                    notification_title = "Examen ajouté"
                    notification_body = f"Un nouvel examen a été ajouté: {examen.title}. Tenez-vous près"
                    send_push_notification(token, notification_title, notification_body)
            form.save_m2m()  # Sauvegarder les cours associés
            messages.success(request, "Examen créé avec succès!")
            return redirect("examen_detail", slug=examen.slug)
    else:
        form = ExamenForm()
    return render(request, "examen/examen_form.html", {"form": form, "title": "Create Exam"})

# Modifier un examen
@login_required
def examen_update(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    if request.method == "POST":
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, _("Examen modifié avec succès!"))
            return redirect("examen_detail", slug=examen.slug)
    else:
        form = ExamenForm(instance=examen)
    return render(request, "examen/examen_form.html", {"form": form, "title": _("Update Exam")})

@login_required
def creer_epreuve(request, examen_slug):
    examen = get_object_or_404(Examen, slug=examen_slug)
    if request.method == 'POST':
        form = EpreuveForm(request.POST,request.FILES)
        if form.is_valid():
            epreuve = form.save(commit=False)
            epreuve.examen = examen  # Associe l'épreuve à l'examen
            epreuve.save()
            return redirect('examen_detail', slug=examen.slug)
    else:
        form = EpreuveForm()
    return render(request, 'examen/creer_epreuve.html', {'form': form, 'examen': examen})

@login_required
@login_required
def epreuve_activation(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    if request.method == 'POST':
        form = EpreuveActivationForm(request.POST, instance=epreuve)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'epreuve '{epreuve.course.title}' a été activé" if epreuve.is_active else f"L'examen '{epreuve.course.title}' a été désactivé.")
            return redirect('examen_detail',epreuve.examen.slug)
    else:
        form = EpreuveActivationForm(instance=epreuve)
    
    return render(request, 'examen/epreuve_activation.html', {
        'form': form,
        'examen': epreuve
    })

@login_required
def epreuve_detail(request, epreuve_id):
    epreuve=get_object_or_404(Epreuve,id=epreuve_id)
    questions = epreuve.questions.all()
    return render(request, "examen/epreuve_detail.html", {"epreuve": epreuve, "questions": questions})

def epreuve_update(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    if request.method == 'POST':
        form = EpreuveForm(request.POST, instance=epreuve)
        if form.is_valid():
            form.save()
            messages.success(request, _("Epreuve modifié avec succès!"))
            return redirect('examen_detail', slug=epreuve.examen.slug)
    else:
        form = EpreuveForm(instance=epreuve)
    return render(request, 'examen/creer_epreuve.html', {'form': form, 'epreuve': epreuve})

def epreuve_delete(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    examen_slug = epreuve.examen.slug  # Sauvegarder le slug de l'examen avant la suppression
    if request.method == 'POST':
        epreuve.delete()
        messages.success(request, f"L'épreuve '{epreuve.course.title}' a été supprimée.")
        return redirect('examen_detail', slug=examen_slug)
    return render(request, 'examen/epreuve_delete.html', {'epreuve': epreuve})


# Supprimer un examen
@login_required
def examen_delete(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    if request.method == "POST":
        examen.delete()
        messages.success(request, _("Examen supprimé avec succès!"))
        return redirect("examen_list")
    return render(request, "examen/examen_confirm_delete.html", {"examen": examen})

# Ajouter une question à un examen@login_required
def question_create(request, epreuve_id):
    epreuve=get_object_or_404(Epreuve, id=epreuve_id)
    if request.method == "POST":
        form = QuestionExamenForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.epreuve = epreuve
            question.save()
            messages.success(request, "Question ajouté avec succès!")
            return redirect("reponse_create", question.id)
    else:
        form = QuestionExamenForm()
    return render(request, "examen/question_form.html", {
        "form": form,
        "title": "Add Question",
        "epreuve": epreuve,
    })

# Modifier une question
@login_required
def question_update(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    if request.method == "POST":
        form = QuestionExamenForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, _("Question modifié avec succès!"))
            return redirect("examen_detail", slug=question.examen.slug)
    else:
        form = QuestionExamenForm(instance=question)
    return render(request, "examen/question_form.html", {"form": form, "title": _("Update Question"), "examen": question.examen})

# Supprimer une question
@login_required
def question_delete(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    examen_slug = question.examen.slug
    if request.method == "POST":
        question.delete()
        messages.success(request, _("Question supprimé avec succès!"))
        return redirect("examen_detail", slug=examen_slug)
    return render(request, "examen/question_confirm_delete.html", {"question": question})

# Ajouter une réponse à une question
@login_required
def reponse_create(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    if request.method == "POST":
        form = ReponseExamenForm(request.POST)
        if form.is_valid():
            
            reponse = form.save(commit=False)
            reponse.question = question
            reponse.save()
            messages.success(request, _("Réponse ajouté avec succès!"))
            return redirect("examen_detail", slug=question.epreuve.examen.slug)
        else:
            print(form.errors)
    else:
        form = ReponseExamenForm()
    return render(request, "examen/reponse_form.html", {"form": form, "title": _("Add Answer"), "question": question})

# Modifier une réponse
@login_required
def reponse_update(request, reponse_id):
    reponse = get_object_or_404(ReponseExamen, id=reponse_id)
    if request.method == "POST":
        form = ReponseExamenForm(request.POST, instance=reponse)
        if form.is_valid():
            form.save()
            messages.success(request, _("Réponse modifié avec succès!"))
            return redirect("examen_detail", slug=reponse.question.examen.slug)
    else:
        form = ReponseExamenForm(instance=reponse)
    return render(request, "examen/reponse_form.html", {"form": form, "title": _("Update Answer"), "question": reponse.question})

# Supprimer une réponse
@login_required
def reponse_delete(request, reponse_id):
    reponse = get_object_or_404(ReponseExamen, id=reponse_id)
    examen_slug = reponse.question.examen.slug
    if request.method == "POST":
        reponse.delete()
        messages.success(request, _("Réponse supprimé avec succès!"))
        return redirect("examen_detail", slug=examen_slug)
    return render(request, "examen/reponse_confirm_delete.html", {"reponse": reponse})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Examen, Epreuve, QuestionExamen, ReponseExamen, Soumission, ResultatExamen
from .forms import ResultatExamenForm

@login_required
def take_examen(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    student = request.user.student
    questions=epreuve.questions.all()

    # Vérifier si l'étudiant a déjà soumis une réponse pour cette épreuve
    if Soumission.objects.filter(student=student, epreuve=epreuve).exists():
        messages.error(request, "Vous avez déjà participé à cette épreuve.")
        return redirect("examen_detail", slug=epreuve.examen.slug)
    
    if not epreuve.is_active:
        messages.error(request, "Cette épreuve n'est pas active.")
        return redirect("examen_detail", slug=epreuve.examen.slug)

    if request.method == "POST":
        if not epreuve.file:
            # Cas où l'épreuve n'a pas de fichier (questions en ligne)
            score = 0

            # Traiter chaque question de l'épreuve
            questions = epreuve.questions.all()
            for question in questions:
                if question.question_type == "multiple_choice":
                    # Pour les questions à choix multiples
                    reponse_id = request.POST.get(f"question_{question.id}")
                    if reponse_id:
                        reponse = get_object_or_404(ReponseExamen, id=reponse_id)
                        if reponse.is_correct:
                            score += question.score

                elif question.question_type == "true_false":
                    # Pour les questions vrai/faux
                    reponse_utilisateur = request.POST.get(f"question_{question.id}")
                    if reponse_utilisateur is not None:
                        reponse_utilisateur = reponse_utilisateur.lower() == "true"
                        reponse_correcte = question.reponses.filter(is_correct=True).first()
                        if reponse_correcte and reponse_utilisateur == reponse_correcte.is_correct:
                            score += question.score

                elif question.question_type == "short_answer":
                    # Pour les questions à réponse courte
                    reponse_utilisateur = request.POST.get(f"question_{question.id}", "").strip().lower()
                    reponse_correcte = question.reponses.filter(is_correct=True).first()
                    if reponse_correcte and reponse_utilisateur == reponse_correcte.content.strip().lower():
                        score += question.score

            # Enregistrer le résultat pour l'épreuve
            ResultatExamen.objects.create(
                student=student,
                epreuve=epreuve,
                score=score,
                is_passed=score >= epreuve.max_score * (epreuve.examen.pass_mark / 100),
            )

            # Enregistrer la soumission pour l'épreuve
            Soumission.objects.create(student=student, epreuve=epreuve)

            messages.success(request, "Vos réponses ont été enregistrées avec succès.")
            return redirect("examen_detail", slug=epreuve.examen.slug)

        else:
            # Cas où l'épreuve a un fichier (soumission manuelle)
            form = ResultatExamenForm(request.POST, epreuve=epreuve)
            if form.is_valid():
                resultat = form.save(commit=False)
                resultat.student = request.user.student  # Associer l'étudiant connecté
                resultat.epreuve = epreuve
                resultat.is_passed=False
                resultat.save()
                Soumission.objects.create(student=request.user.student,epreuve=epreuve)
                messages.success(request,"Vous reponses ont été envoyée. Votre moyenne sera disponible dans quelques temps")
                return redirect("examen_detail",epreuve.examen.slug)
                
            else:
                messages.error(request,"erreur")

    else:
        form = ResultatExamenForm(epreuve=epreuve)
        # Afficher le formulaire pour passer l'épreuve
        if not epreuve.file:
            # Cas où l'épreuve n'a pas de fichier (questions en ligne)
            return render(request, "examen/take_examen.html", {"epreuve": epreuve, "form": form,"questions":questions})
        else:
            # Cas où l'épreuve a un fichier (soumission manuelle)
            return render(request, "examen/soumettre_examen.html", {"epreuve": epreuve, "form": form})

@login_required
@lecturer_required
def correction_examens(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    lecturer = get_object_or_404(Lecturer, user=request.user)
    resultats = ResultatExamen.objects.filter(
        epreuve=epreuve,
        student__in=lecturer.students.all()  # Utiliser la relation many-to-many
    ).select_related("student")

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("score_"):
                resultat_id = key.split("_")[1]
                resultat = ResultatExamen.objects.get(id=resultat_id)
                resultat.score = float(value)
                resultat.corrected_by_teacher = True
                resultat.save()
        return redirect("examen_detail", slug=epreuve.examen.slug)

    return render(request, "examen/corriger_examens.html", {"epreuve": epreuve, "resultats": resultats})


# Voir les résultats d'un examen
@login_required
def epreuve_results(request, epreuve_id):
    epreuve=get_object_or_404(Epreuve, id=epreuve_id)
    results = ResultatExamen.objects.filter(epreuve=epreuve).order_by("-score")

    return render(request, "examen/epreuve_results.html", {
        "epreuve": epreuve,
        "results": results,
    })


def notes_et_moyennes_examen(request, examen_slug):
    # Récupérer l'examen
    examen = get_object_or_404(Examen, slug=examen_slug)

    # Récupérer toutes les épreuves actives de l'examen
    epreuves = examen.epreuves.filter(is_active=True)

    # Récupérer tous les étudiants ayant participé à l'examen
    etudiants = Student.objects.filter(
        resultatexamen__epreuve__examen=examen
    ).distinct()

    # Préparer les données pour le template
    donnees_etudiants = []
    for etudiant in etudiants:
        # Récupérer les résultats de l'étudiant pour chaque épreuve
        resultats_etudiant = []
        for epreuve in epreuves:
            resultat = ResultatExamen.objects.filter(
                student=etudiant, epreuve=epreuve
            ).first()
            resultats_etudiant.append({
                "epreuve": epreuve,
                "resultat": resultat,
            })

        # Calculer la moyenne de l'étudiant pour l'examen
        moyenne_etudiant = ResultatExamen.objects.filter(
            student=etudiant, epreuve__examen=examen
        ).aggregate(moyenne=Avg('score'))['moyenne']

        # Ajouter les données de l'étudiant à la liste
        donnees_etudiants.append({
            "etudiant": etudiant,
            "resultats": resultats_etudiant,
            "moyenne": moyenne_etudiant,
        })

    return render(request, "examen/notes_et_moyennes.html", {
        "examen": examen,
        "donnees_etudiants": donnees_etudiants,
        "epreuves": epreuves,
    })