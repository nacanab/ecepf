from .utils import (
    generate_student_credentials,
    generate_lecturer_credentials,
    send_new_account_email,
)
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSession
from django.db.models.signals import post_save


def post_save_account_receiver(instance=None, created=False, *args, **kwargs):
    """
    Send email notification
    """
    if created:
        if instance.is_student:
            username, password = generate_student_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            # Send email with the generated credentials
            send_new_account_email(instance, password)

        if instance.is_lecturer:
            username, password = generate_lecturer_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            # Send email with the generated credentials
            send_new_account_email(instance, password)



@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Créer une session utilisateur lors de la connexion."""
    UserSession.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Mettre à jour la session utilisateur lors de la déconnexion."""
    last_session = UserSession.objects.filter(user=user, logout_time__isnull=True).last()
    if last_session:
        last_session.logout_time = timezone.now()
        last_session.save()


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from result.models import TakenCourse
from .models import StudentLogs
from course.models import Course

@receiver(post_save, sender=TakenCourse)
def log_course_registration(sender, instance, created, **kwargs):
    """
    Enregistre un log lorsqu'un étudiant s'inscrit à un cours.
    """
    if created:  # Vérifie si l'objet TakenCourse vient d'être créé
        StudentLogs.objects.create(
            student=instance.student,
            message=f"L'étudiant s'est inscrit au cours '{instance.course.title}'.",
            activity_type="course_registration",
        )

from django.db.models.signals import post_save
from django.dispatch import receiver
from quiz.models import Sitting
from .models import StudentLogs

@receiver(post_save, sender=Sitting)
def log_quiz_completion(sender, instance, **kwargs):
    if instance.complete:  # Vérifie si le quiz est terminé
        StudentLogs.objects.create(
            student=instance.user.student,
            message=f"L'étudiant a terminé le quiz '{instance.quiz.title}'.",
            activity_type="quiz_completion",
        )