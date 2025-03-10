from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from course.models import Course
from core.utils import unique_slug_generator
from accounts.models import Student

class Examen(models.Model):
    courses = models.ManyToManyField(Course, verbose_name=_("Cours"))  # Changé pour ManyToManyField
    title = models.CharField(verbose_name=_("Titre"), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    date = models.DateTimeField(verbose_name=_("Date d'examen"))
    duration = models.IntegerField(verbose_name=_("Durée (minutes)"))
    max_score = models.IntegerField(verbose_name=_("Score maximum"), default=100)
    pass_mark = models.IntegerField(verbose_name=_("Score de passage"), default=50)
    is_active = models.BooleanField(default=False, verbose_name=_("Est actif"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="exam_files/", blank=True, null=True, verbose_name=_("Fichier d'examen"))

    def __str__(self):
        return f"{self.title} - {', '.join([course.title for course in self.courses.all()])}"

    def get_absolute_url(self):
        return reverse("examen_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")



class QuestionExamen(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name="questions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("Cours"))  # Ajout d'une clé étrangère vers Course
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
    question = models.ForeignKey(QuestionExamen, on_delete=models.CASCADE, related_name="reponses")
    content = models.TextField(verbose_name=_("Answer Content"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    def __str__(self):
        return f"{self.content[:50]}..."

    class Meta:
        verbose_name = _("Exam Answer")
        verbose_name_plural = _("Exam Answers")

class ResultatExamen(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Student"))
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, verbose_name=_("Exam"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("Cours"))  # Ajout d'une clé étrangère vers Course
    score = models.FloatField(verbose_name=_("Score"))
    is_passed = models.BooleanField(default=False, verbose_name=_("Is Passed"))
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.examen} - {self.course} - {self.score}"

    class Meta:
        verbose_name = _("Exam Result")
        verbose_name_plural = _("Exam Results")