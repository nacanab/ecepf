from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, lecturer_required,parent_required
from accounts.models import User, Student, Lecturer, UserProfile
from config.firebase_utils import send_push_notification
from examen.models import Examen
from .forms import SessionForm, SemesterForm, NewsAndEventsForm
from .models import NewsAndEvents, ActivityLog, Session, Semester
from course.models import Course,CourseAllocation, Upload, UploadVideo
from accounts.models import UserSession
from django.utils import timezone
from accounts.models import Parent
from result.models import TakenCourse
from quiz.models import Sitting,Quiz
from accounts.models import StudentLogs

# ########################################################
# News & Events
# ########################################################
def accueil(request):
    return render(request, 'accounts/acceuil.html')

@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")
    context = {
        "title": "News & Events",
        "items": items,
    }
    return render(request, "core/index.html", context)


@login_required
@admin_required
def dashboard_view(request):
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    gender_count = Student.get_gender_count()
    context = {
        "student_count": User.objects.get_student_count(),
        "lecturer_count": User.objects.get_lecturer_count(),
        "superuser_count": User.objects.get_superuser_count(),
        "males_count": gender_count["M"],
        "females_count": gender_count["F"],
        "logs": logs,
        "parents_count": Parent.objects.all().count(),
        "fiches":Upload.objects.all().count(),
        "videos":UploadVideo.objects.all().count(),
        "quiz":Quiz.objects.all().count(),
        "examen":Examen.objects.all().count(),
    }
    return render(request, "core/dashboard.html", context)



@login_required
@lecturer_required
def lecturer_dashboard_view(request):
    lecturer = Lecturer.objects.get(user=request.user)
    course_count=CourseAllocation.objects.filter(lecturer=lecturer).count()
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    males_count=lecturer.get_male_count()
    females_count=lecturer.get_female_count()
    context = {
        "student_count": lecturer.students.count(),
        "student_total_count":Student.objects.all().count(),
        "course_count": course_count,
        "superuser_count": User.objects.get_superuser_count(),
        "males_count": males_count,
        "females_count": females_count,
        "logs": logs,
        "fiches":Upload.objects.all().count(),
        "videos":UploadVideo.objects.all().count(),
        "quiz":Quiz.objects.all().count(),
        "examen":Examen.objects.all().count(),
    }
    return render(request, "core/dashboard.html", context)



@login_required
def total_connected_time(request):
    user = request.user
    sessions = UserSession.objects.filter(user=user)
    total_time = sum(
        (session.logout_time - session.login_time).total_seconds()
        for session in sessions
        if session.logout_time
    )
    return render(request, 'total_connected_time.html', {
        'total_time': total_time
    })


    


@login_required
@parent_required
def parent_dashboard_view(request):
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    gender_count = Student.get_gender_count()
    courses_count=Course.objects.all().count()


    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        # Si l'utilisateur connecté n'est pas un parent, afficher un message d'erreur
        return render(request, 'error.html', {'message': 'Vous n\'êtes pas un parent.'})
    student = parent.student
    number_of_courses_taken = TakenCourse.objects.filter(student_id=student.id).count()
    quiz_count = Sitting.objects.filter(user=student.student, complete=True).count()
    total_quiz_count = Quiz.objects.count()
    studentlogs = StudentLogs.objects.filter(student_id=student.id).order_by("-timestamp")

    total_seconds = student.student.get_total_time_spent()

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    #total_time=total_time.strftime("%H:%M:%S")
    context = {
        "student_count": number_of_courses_taken,
        "courses_count": courses_count,
        "lecturer_count": User.objects.get_lecturer_count(),
        "superuser_count": User.objects.get_superuser_count(),
        "total_time": f"{int(hours)}h {int(minutes)}m {int(seconds)}s",
        "quiz_count": quiz_count,
        "total_quiz_count": total_quiz_count,
        "logs": logs,
        "studentlogs": studentlogs,
    }

    return render(request, "core/dashboard.html", context)




@login_required
def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST)
        title = form.cleaned_data.get("title", "Post") if form.is_valid() else None
        if form.is_valid():
            form.save()
            user_profiles = UserProfile.objects.all()  # Récupérer tous les utilisateurs
            for profile in user_profiles:
                token = profile.firebase_token
                if token:
                    # Envoyer une notification
                    notification_title = "Nouveau post ajouté"
                    notification_body = f"Un nouveau post a été ajouté : {title}"
                    send_push_notification(token, notification_title, notification_body)
            messages.success(request, f"{title} a été ajouté.")
            return redirect("home")
        messages.error(request, "SVP corrigez les erreurs.")
    else:
        form = NewsAndEventsForm()
    return render(request, "core/post_add.html", {"title": "Add Post", "form": form})


@login_required
@lecturer_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = form.cleaned_data.get("title", "Post") if form.is_valid() else None
        if form.is_valid():
            form.save()
            messages.success(request, f"{title} a été ajouté.")
            return redirect("home")
        messages.error(request, "SVP corrigez les erreurs.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(request, "core/post_add.html", {"title": "Edit Post", "form": form})


@login_required
@lecturer_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    post_title = post.title
    post.delete()
    messages.success(request, f"{post_title} has been deleted.")
    return redirect("home")


# ########################################################
# Session
# ########################################################
@login_required
@lecturer_required
def session_list_view(request):
    """Show list of all sessions"""
    sessions = Session.objects.all().order_by("-is_current_session", "-session")
    return render(request, "core/session_list.html", {"sessions": sessions})


@login_required
@lecturer_required
def session_add_view(request):
    """Add a new session"""
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("is_current_session"):
                unset_current_session()
            form.save()
            messages.success(request, "Année scolaire ajouté.")
            return redirect("session_list")
    else:
        form = SessionForm()
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_update_view(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            if form.cleaned_data.get("is_current_session"):
                unset_current_session()
            form.save()
            messages.success(request, "Année scolaire mise à jour.")
            return redirect("session_list")
    else:
        form = SessionForm(instance=session)
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if session.is_current_session:
        messages.error(request, "Vous ne pouvez pas supprimer l'année scolaire en cours.")
    else:
        session.delete()
        messages.success(request, "Année scolaire supprimé avec succès.")
    return redirect("session_list")


def unset_current_session():
    """Unset current session"""
    current_session = Session.objects.filter(is_current_session=True).first()
    if current_session:
        current_session.is_current_session = False
        current_session.save()


# ########################################################
# Semester
# ########################################################
@login_required
@lecturer_required
def semester_list_view(request):
    semesters = Semester.objects.all().order_by("-is_current_semester", "-semester")
    return render(request, "core/semester_list.html", {"semesters": semesters})


@login_required
@lecturer_required
def semester_add_view(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("is_current_semester"):
                unset_current_semester()
                unset_current_session()
            form.save()
            messages.success(request, "Trimestre ajouté avec succès.")
            return redirect("semester_list")
    else:
        form = SemesterForm()
    return render(request, "core/semester_update.html", {"form": form})


@login_required
@lecturer_required
def semester_update_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == "POST":
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            if form.cleaned_data.get("is_current_semester"):
                unset_current_semester()
                unset_current_session()
            form.save()
            messages.success(request, "Trimestre mis à jour!")
            return redirect("semester_list")
    else:
        form = SemesterForm(instance=semester)
    return render(request, "core/semester_update.html", {"form": form})


@login_required
@lecturer_required
def semester_delete_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester:
        messages.error(request, "Vous ne pouvez pas supprimer le trimestre actuel.")
    else:
        semester.delete()
        messages.success(request, "Trimestre supprimé avec succès.")
    return redirect("semester_list")


def unset_current_semester():
    """Unset current semester"""
    current_semester = Semester.objects.filter(is_current_semester=True).first()
    if current_semester:
        current_semester.is_current_semester = False
        current_semester.save()
