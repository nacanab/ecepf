from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from course.models import Course
from accounts.models import Student

class Examen(models.Model):
    title = models.CharField(verbose_name=_("Titre"), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    date = models.DateTimeField(verbose_name=_("Date d'examen"))
    pass_mark = models.IntegerField(verbose_name=_("Score de passage"), default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("examen_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")


class Epreuve(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name="epreuves")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("Cours"))
    is_active = models.BooleanField(default=False, verbose_name=_("Est actif"))
    max_score = models.IntegerField(verbose_name=_("Note maximum"), default=10)
    file = models.FileField(upload_to="exam_files/", blank=True, null=True, verbose_name=_("Fichier d'epreuve"))
    duration = models.IntegerField(verbose_name=_("Durée (minutes)"))

    def __str__(self):
        return f"{self.course.title} (Examen: {self.examen.title})"

    class Meta:
        verbose_name = _("Épreuve")
        verbose_name_plural = _("Épreuves")
        unique_together = ('examen', 'course')


class QuestionExamen(models.Model):
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE, related_name="questions",null=True,blank=True)
    content = models.TextField(verbose_name=_("Question Content"))
    question_type = models.CharField(
        max_length=20,
        choices=[
            ("multiple_choice", _("Multiple Choice")),
            ("true_false", _("True/False")),
            ("short_answer", _("Short Answer")),
        ],
        default="multiple_choice",
        verbose_name=_("Question Type"),
    )
    score = models.IntegerField(verbose_name=_("Score"), default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content[:50]}..."

    class Meta:
        verbose_name = _("Exam Question")
        verbose_name_plural = _("Exam Questions")


class ReponseExamen(models.Model):
    question = models.ForeignKey(QuestionExamen, on_delete=models.CASCADE, related_name="reponses",blank=True, null=True)
    content = models.TextField(verbose_name=_("Answer Content"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    def __str__(self):
        return f"{self.content[:50]}..."

    class Meta:
        verbose_name = _("Exam Answer")
        verbose_name_plural = _("Exam Answers")


class Soumission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE)
    soumission_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} a répondu à l'épreuve {self.epreuve} à {self.soumission_date}"

    class Meta:
        verbose_name = _("Soumission")
        verbose_name_plural = _("Soumissions")


class ResultatExamen(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Student"))
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE, verbose_name=_("Épreuve"))
    score = models.FloatField(verbose_name=_("Score"), null=True, blank=True)
    is_passed = models.BooleanField(default=False, verbose_name=_("Is Passed"))
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    reponse_text = models.TextField(verbose_name=_("Réponse de l'élève"), blank=True, null=True)
    corrected_by_teacher = models.BooleanField(default=False, verbose_name=_("Corrigé par l'enseignant"))

    def __str__(self):
        return f"{self.student} - {self.epreuve} - {self.score if self.score is not None else 'Non noté'}"

    class Meta:
        verbose_name = _("Exam Result")
        verbose_name_plural = _("Exam Results")