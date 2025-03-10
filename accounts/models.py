from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from PIL import Image
from core.models import ActivityLog
from course.models import Program,Course
from .validators import ASCIIUsernameValidator
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Sum
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.utils import timezone




FATHER = _("Père")
MOTHER = _("Mère")
BROTHER = _("Frère")
SISTER = _("Soeur")
GRAND_MOTHER = _("Grand-mère")
GRAND_FATHER = _("Grand-père")
OTHER = _("Autre")

RELATION_SHIP = (
    (FATHER, _("Père")),
    (MOTHER, _("Mère")),
    (BROTHER, _("Frère")),
    (SISTER, _("Soeur")),
    (GRAND_MOTHER, _("Grand-mère")),
    (GRAND_FATHER, _("Grand-père")),
    (OTHER, _("Autre")),
)


class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset

    def get_student_count(self):
        return self.model.objects.filter(is_student=True).count()

    def get_lecturer_count(self):
        return self.model.objects.filter(is_lecturer=True).count()

    def get_superuser_count(self):
        return self.model.objects.filter(is_superuser=True).count()


GENDERS = ((_("M"), _("Masculin")), (_("F"), _("Féminin")))


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_dep_head = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(
        upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    )
    email = models.EmailField(blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    objects = CustomUserManager()

    class Meta:
        ordering = ("-date_joined",)

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            role = _("Admin")
        elif self.is_student:
            role = _("Student")
        elif self.is_lecturer:
            role = _("Lecturer")
        elif self.is_parent:
            role = _("Parent")

        return role

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"user_id": self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + "default.png":
            self.picture.delete()
        super().delete(*args, **kwargs)

    def get_total_time_spent(self):
        """Retourne le temps total passé par l'utilisateur sur la plateforme en secondes."""
        total_seconds = UserSession.objects.filter(user=self).aggregate(
            total_time=Sum(models.F('logout_time') - models.F('login_time'))
        )['total_time']

        return total_seconds.total_seconds() if total_seconds else 0  # Retourne 0 si aucune session


User = get_user_model()

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)

    def get_session_duration(self):
        """Retourne la durée de la session en secondes."""
        if self.logout_time:
            return (self.logout_time - self.login_time).total_seconds()
        return 0  # Si pas encore déconnecté

    def __str__(self):
        return f"{self.user.username} - {self.login_time} to {self.logout_time}"
    
    def is_online(self):
        return (timezone.now() - self.last_activity).total_seconds() < 300  # 5 minutes

    def get_last_activity(self):
        if self.is_online():
            return "En ligne"
        return f"Dernière connexion : {self.last_activity.strftime('%d/%m/%Y %H:%M')}"


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = Q(level__icontains=query) | Q(program__icontains=query)
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs

    

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name="students", blank=True)
    bio = models.TextField(blank=True, null=True)
    is_assigned = models.BooleanField(default=False)
    objects = StudentManager()

    class Meta:
        ordering = ("-student__date_joined",)

    def __str__(self):
        return self.student.get_full_name

    @classmethod
    def get_gender_count(cls):
        males_count = Student.objects.filter(student__gender="M").count()
        females_count = Student.objects.filter(student__gender="F").count()

        return {"M": males_count, "F": females_count}

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"user_id": self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)
    
    def get_total_time_spent(self):
        """Retourne le temps total passé en secondes."""
        total_seconds = UserSession.objects.filter(user=self.student).aggregate(
            total_time=Sum(models.F('logout_time') - models.F('login_time'))
        )['total_time']
        
        return total_seconds.total_seconds() if total_seconds else 0  # Retourne 0 si aucune session
    

@receiver(m2m_changed, sender=Student.courses.through)
def log_student_course_activity(sender, instance, action, **kwargs):
    if action == "post_add":
        for course_id in kwargs.get('pk_set', []):
            course = Course.objects.get(id=course_id)
            ActivityLog.objects.create(
                message=_(f"L'étudiant '{instance.èstudent.get_full_name}' s'est inscrit au cours '{course.title}'.")
            )

class StudentLogs(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_logs"
    )
    message = models.CharField(max_length=255)
    activity_type = models.CharField(
        max_length=50,
        choices=(
            ("course_registration", _("Inscription à un cours")),
            ("quiz_completion", _("Quiz terminé")),
            ("login", _("Connexion")),
            ("logout", _("Déconnexion")),
            ("other", _("Autre")),
        ),
        default="other",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("Student Log")
        verbose_name_plural = _("Student Logs")

    def __str__(self):
        return f"{self.student.student.get_full_name()} - {self.activity_type} - {self.timestamp}"

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer_profile")
    students = models.ManyToManyField(Student, blank=True)  # Ajout de la relation
    def __str__(self):
        return self.user.get_full_name()
    def get_male_count(self):
        return self.students.filter(student__gender='M').count()

    def get_female_count(self):
        return self.students.filter(student__gender='F').count()




class Parent(models.Model):
    """
    Connect student with their parent, parents can
    only view their connected students information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # What is the relationship between the student and
    # the parent (i.e. father, mother, brother, sister)
    relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return self.user.username
    
    def get_student_name(self):
        return self.student.student.get_full_name()
    
    def get_student_sessions(self):
        """
        Récupère toutes les sessions de l'étudiant associé à ce parent.
        """
        if self.student:
            return UserSession.objects.filter(user=self.student.student)
        return UserSession.objects.none()  # Retourne un queryset vide si aucun étudiant n'est associé




class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return "{}".format(self.user)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firebase_token = models.CharField(max_length=255, blank=True, null=True)


class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
