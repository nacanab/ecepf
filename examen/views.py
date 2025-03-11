from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Examen, QuestionExamen, ReponseExamen, ResultatExamen
from .forms import ExamenForm, QuestionExamenForm, ReponseExamenForm,ExamenActivationForm
from django.utils.text import slugify
from accounts.models import UserProfile
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
    questions = examen.questions.all()
    return render(request, "examen/examen_detail.html", {"examen": examen, "questions": questions})

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
            messages.success(request, "Examen ajouté avec succès!")
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
            messages.success(request, _("Examen mis à jour avec succès!"))
            return redirect("examen_detail", slug=examen.slug)
    else:
        form = ExamenForm(instance=examen)
    return render(request, "examen/examen_form.html", {"form": form, "title": _("Update Exam")})





@login_required
def examen_activation(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    if request.method == 'POST':
        form = ExamenActivationForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'examen '{examen.title}' a été activé" if examen.is_active else f"L'examen '{examen.title}' a été désactivé.")
            return redirect('examen_list')
    else:
        form = ExamenActivationForm(instance=examen)
    
    return render(request, 'examen/examen_activation.html', {
        'form': form,
        'examen': examen
    })






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
def question_create(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    if request.method == "POST":
        form = QuestionExamenForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.examen = examen
            question.save()
            messages.success(request, "Question ajouté avec succès!")
            return redirect("examen_detail", slug=examen.slug)
    else:
        form = QuestionExamenForm()
    return render(request, "examen/question_form.html", {
        "form": form,
        "title": "Add Question",
        "examen": examen,
        "courses": examen.courses.all(),  # Passer la liste des cours associés
    })

# Modifier une question
@login_required
def question_update(request, question_id):
    question = get_object_or_404(QuestionExamen, id=question_id)
    if request.method == "POST":
        form = QuestionExamenForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, _("Question mis à jour avec succès!"))
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
            return redirect("examen_detail", slug=question.examen.slug)
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
            messages.success(request, _("Réponse mis à jour avec succès!"))
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
        messages.success(request, _("Réponse supprimée avec succès!"))
        return redirect("examen_detail", slug=examen_slug)
    return render(request, "examen/reponse_confirm_delete.html", {"reponse": reponse})

@login_required
def take_examen(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    questions = examen.questions.all()

    if request.method == "POST":
        score = 0
        total_questions = questions.count()

        # Traiter chaque question
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

        # Enregistrer le résultat pour chaque cours associé à l'examen
        for course in examen.courses.all():
            ResultatExamen.objects.create(
                student=request.user.student,
                examen=examen,
                course=course,  # Ajouter le cours associé
                score=score,
                is_passed=score >= examen.pass_mark,
            )

        messages.success(request, _("Examen soumis!"))
        return redirect("examen_results", slug=examen.slug)

    return render(request, "examen/take_examen.html", {"examen": examen, "questions": questions})
# Voir les résultats d'un examen
@login_required
def examen_results(request, slug):
    examen = get_object_or_404(Examen, slug=slug)
    course_id = request.GET.get("course_id")  # Récupérer le cours sélectionné

    if course_id:
        results = ResultatExamen.objects.filter(examen=examen, course_id=course_id).order_by("-score")
    else:
        results = ResultatExamen.objects.filter(examen=examen).order_by("-score")

    return render(request, "examen/examen_results.html", {
        "examen": examen,
        "results": results,
        "courses": examen.courses.all(),  # Passer la liste des cours associés
    })