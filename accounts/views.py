from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django_filters.views import FilterView
from xhtml2pdf import pisa
from django.contrib.auth.hashers import check_password
from accounts.decorators import admin_required,lecturer_required
from accounts.filters import LecturerFilter, StudentFilter
from accounts.forms import (
    ParentAddForm,
    ProfileUpdateForm,
    ProgramUpdateForm,
    StaffAddForm,
    StudentAddForm,
)
from accounts.models import Parent, Student, User
from badges.models import AttributionBadge
from core.models import Semester, Session
from course.models import Course,CourseAllocation
from result.models import TakenCourse
from .utils import send_new_account_email
from .utils import generate_password
from django.http import JsonResponse
from config.firebase_utils import send_push_notification
from .models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Lecturer
from .forms import AssignStudentsForm
# ########################################################
# Utility Functions
# ########################################################

def accueil(request):
    return render(request, 'accounts/acceuil.html')

def render_to_pdf(template_name, context):
    """Render a given template to PDF format."""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="profile.pdf"'
    template = render_to_string(template_name, context)
    pdf = pisa.CreatePDF(template, dest=response)
    if pdf.err:
        return HttpResponse("Nous rencontrons un probème pour générer le PDF")
    return response


# ########################################################
# Authentication and Registration
# ########################################################


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)

from django.shortcuts import render, redirect
from .forms import RoleForm

def choose_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            return redirect('register', role=role)
    else:
        form = RoleForm()
    return render(request, 'registration/role_selection.html', {'form': form})

def register(request,role):
    if role == "student":
        if request.method == "POST":
            form = StudentAddForm(request.POST)
            if form.is_valid():
                student=form.save()
                full_name=student.get_full_name
                email=student.email
                messages.success(
                    request,
                    f"Un compte pour l'élève {full_name} a été créé. "
                    f"Un mail avec vos informations de connexion a été envoyé à l'adresse {email}."
                    f"Songez à modifier vos informations de connexion,une fois connecté.",
                )
                return redirect("login")
            messages.error(
                request, "Assurez-vous que tout les champs sont bien remplis!"
            )
        else:
            form = StudentAddForm()
        return render(request, "registration/student_register.html", {"form": form})
    
    elif role=="parent":
        if request.method == "POST":
            a=0
            form = ParentAddForm(request.POST)
            if form.is_valid():
                a=1
                if form.cleaned_data.get("student").student.check_password(form.cleaned_data.get("student_password")):
                    form.save()
                    messages.success(request, "Compte créé avc succès.")
                    return redirect("login")
            if a==0:
                messages.error(
                    request, "Assurez-vous que tout les champs sont bien remplis"
                )
            else:
                messages.error(
                    request, "Verifier le mot de passe de l'etudiant"
                )
        else:
            form = ParentAddForm()
        return render(request, "registration/parent_register.html", {"form": form})
    elif role=="lecturer":
        if request.method == "POST":
            form = StaffAddForm(request.POST)
            if form.is_valid():
                lecturer = form.save()
                full_name = lecturer.get_full_name
                email = lecturer.email
                messages.success(
                    request,
                    f"Un compte pour l'enseignant {full_name} a été créé. "
                    f"Un mail avec vos informations de connexion a été envoyé à l'adresse {email}."
                    f"Songez à modifier vos informations de connexion, une fois connecté.",
                )
                return redirect("login")
        else:
            form = StaffAddForm()
        return render(
            request, "registration/lecturer_register.html", {"title": "Add Lecturer", "form": form}
        )


# ########################################################
# Profile Views
# ########################################################


@login_required
def profile(request):
    """Show profile of the current user."""
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    context = {
        "title": request.user.get_full_name,
        "current_session": current_session,
        "current_semester": current_semester,
    }

    if request.user.is_lecturer:
        courses = Course.objects.filter(
            allocated_course__lecturer__pk=request.user.id, semester=current_semester
        )
        context["courses"] = courses
        return render(request, "accounts/profile.html", context)

    if request.user.is_student:
        student = get_object_or_404(Student, student__pk=request.user.id)
        badges=AttributionBadge.objects.filter(student_id=7)
        parent = Parent.objects.filter(student=student).first()
        courses = TakenCourse.objects.filter(
            student__student__id=request.user.id
        )
        context.update(
            {
                "parent": parent,
                "courses": courses,
                "badges": badges,
            }
        )
        return render(request, "accounts/profile.html", context)

    # For superuser or other staff
    staff = User.objects.filter(is_lecturer=True)
    context["staff"] = staff
    return render(request, "accounts/profile.html", context)


@login_required
def child_profile(request):
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()
    # Récupérer le parent connecté
    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        # Si l'utilisateur connecté n'est pas un parent, afficher un message d'erreur
        return render(request, 'error.html', {'message': 'Vous n\'êtes pas un parent.'})
    
    # Récupérer l'étudiant (enfant) associé à ce parent
    student = parent.student
    
    # Récupérer les informations du profil de l'étudiant
    student_name = student.student.get_full_name
    student_level = student.level
    student_gender = student.student.gender
    student_email = student.student.email
    student_phone = student.student.phone
    student_address = student.student.address
    student_picture = student.student.get_picture()
    
    # Récupérer les cours suivis par l'étudiant
    courses = TakenCourse.objects.filter(student=student)
    
    # Passer les informations au template
    context = {
        'title': f"Profil de {student_name}",
        'student_name': student_name,
        'student_level': student_level,
        'student_gender': student_gender,
        'student_email': student_email,
        'student_phone': student_phone,
        'student_address': student_address,
        'title': f"Profil de {student_name}",
        'student_name': student_name,
        'student_picture': student_picture,
        'student': student,
        'courses': courses,
        'current_semester': current_semester,
        'current_session': current_session,
}
    
    return render(request, 'accounts/child_profile.html', context)

@login_required
@admin_required
def profile_single(request, user_id):
    """Show profile of any selected user."""
    if request.user.id == user_id:
        return redirect("profile")

    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()
    user = get_object_or_404(User, pk=user_id)

    context = {
        "title": user.get_full_name,
        "user": user,
        "current_session": current_session,
        "current_semester": current_semester,
    }

    if user.is_lecturer:
        courses = Course.objects.filter(
            allocated_course__lecturer__pk=user_id, semester=current_semester
        )
        context.update(
            {
                "user_type": "Lecturer",
                "courses": courses,
            }
        )
    elif user.is_student:
        student = get_object_or_404(Student, student__pk=user_id)
        courses = TakenCourse.objects.filter(
            student__student__id=user_id,
        )
        context.update(
            {
                "user_type": "Student",
                "courses": courses,
                "student": student,
            }
        )
    else:
        context["user_type"] = "Superuser"

    if request.GET.get("download_pdf"):
        return render_to_pdf("pdf/profile_single.html", context)

    return render(request, "accounts/profile_single.html", context)


@login_required
@admin_required
def admin_panel(request):
    return render(request, "setting/admin_panel.html", {"title": "Admin Panel"})


# ########################################################
# Settings Views
# ########################################################


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil e été mis à jour.")
            return redirect("profile")
        messages.error(request, "SVP corrigez les erreurs.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "setting/profile_info_change.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été bien mis à jour!")
            return redirect("profile")
        messages.error(request, "SVP corrigez les erreurs.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "setting/password_change.html", {"form": form})


# ########################################################
# Staff (Lecturer) Views
# ########################################################


@login_required
@admin_required
def staff_add_view(request):
    if request.method == "POST":
        form = StaffAddForm(request.POST)
        if form.is_valid():
            lecturer = form.save()
            full_name = lecturer.get_full_name
            email = lecturer.email
            messages.success(
                request,
                f"Un compte enseignant pour {full_name} a été crée. "
                f" Un mail avec les informations de connexion a été envoyé à l'adresse {email}.",
            )
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()
    return render(
        request, "accounts/add_staff.html", {"title": "Add Lecturer", "form": form}
    )



@login_required
@admin_required
def assign_students(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, user_id=lecturer_id)
    if request.method == "POST":
        form = AssignStudentsForm(request.POST, instance=lecturer)
        if form.is_valid():
            selected_students = form.cleaned_data['students']

            # Ajouter les étudiants sélectionnés à l'enseignant
            lecturer.students.add(*selected_students)
            for student in lecturer.students.all():
                student.is_assigned = True
                student.save()

            messages.success(request, "Les étudiants ont été assignés avec succès !")
            return redirect("lecturer_assign_list")  # Redirige vers une page listant les enseignants
    else:
        form = AssignStudentsForm(instance=lecturer)

    return render(request, "lecturer/assign_students.html", {"form": form, "lecturer": lecturer})


@login_required
@admin_required
def desasign_student(request,lecturer_id,student_id):
    lecturer = get_object_or_404(Lecturer, user_id=lecturer_id)
    student = get_object_or_404(Student, student_id=student_id)
    lecturer.students.remove(student)
    student.is_assigned = False
    student.save()
    messages.success(request, "L'étudiant a été désassigné avec succès.")
    return redirect("lecturer_student_list",lecturer_id)


@login_required
@admin_required
def edit_staff(request, pk):
    lecturer = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=lecturer)
        if form.is_valid():
            form.save()
            full_name = lecturer.get_full_name
            messages.success(request, f"L'enseignant {full_name} a été mis à jour.")
            return redirect("lecturer_list")
        messages.error(request, "SVP corrigez les erreurs.")
    else:
        form = ProfileUpdateForm(instance=lecturer)
    return render(
        request, "accounts/edit_lecturer.html", {"title": "Edit Lecturer", "form": form}
    )


@method_decorator([login_required, admin_required], name="dispatch")
class LecturerFilterView(FilterView):
    filterset_class = LecturerFilter
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lecturers"
        return context


@login_required
@admin_required
def render_lecturer_pdf_list(request):
    lecturers = User.objects.filter(is_lecturer=True)
    template_path = "pdf/lecturer_list.html"
    context = {"lecturers": lecturers}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="lecturers_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f"Nous avons quelques erreurs <pre>{html}</pre>")
    return response


@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, is_lecturer=True, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, f"L'enseignant {full_name} a été supprimé.")
    return redirect("lecturer_list")


# ########################################################
# Student Views
# ########################################################


@login_required
@admin_required
def student_add_view(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            student = form.save()
            full_name = student.get_full_name
            email = student.email
            messages.success(
                request,
                f"Un compte élève pour {full_name} a été crée. "
                f" Un mail avec les informations de connexion a été envoyé à l'adresse {email}.",
            )
            return redirect("student_list")
        for field, errors in form.errors.items():
            messages.error(request, f"Champ '{field}' non renseigné ou invalide : {errors}")
    else:
        form = StudentAddForm()
    return render(
        request, "accounts/add_student.html", {"title": "Add Student", "form": form}
    )


@login_required
@admin_required
def edit_student(request, pk):
    student_user = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=student_user)
        if form.is_valid():
            form.save()
            full_name = student_user.get_full_name
            messages.success(request, f"Student {full_name} has been updated.")
            return redirect("student_list")
        messages.error(request, "SVP sorrigez les erreurs")
    else:
        form = ProfileUpdateForm(instance=student_user)
    return render(
        request, "accounts/edit_student.html", {"title": "Edit Student", "form": form}
    )


@method_decorator([login_required, admin_required], name="dispatch")
class StudentListView(FilterView):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    template_name = "accounts/student_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students"
        return context
    

@login_required
@lecturer_required
def student_list(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, user_id=lecturer_id)
    students=lecturer.students.all().order_by('student__last_name','student__first_name')
    count=lecturer.students.count()
    return render(request, 'lecturer/lecturer_student_list.html', {'students': students, 'count': count,'lecturer':lecturer})

@login_required
@admin_required
def lecturer_assign_list(request):
    lecturers=User.objects.filter(is_lecturer=True)
    count=User.objects.filter(is_lecturer=True).count()
    return render(request, 'lecturer/lecturers.html', {'lecturers':lecturers,'count':count})


@login_required
@lecturer_required
def student_single(request, user_id):
    """Show profile of any selected user."""
    if request.user.id == user_id:
        return redirect("profile")

    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()
    user = get_object_or_404(User, pk=user_id)
    student = get_object_or_404(Student, student__pk=user_id)
    stu=Student.objects.filter(id=user_id)
    courses = TakenCourse.objects.filter(
        student__student__id=user_id,
    )
    badges=AttributionBadge.objects.filter(student=student)
    context = {
        "title": user.get_full_name,
        "user": user,
        "current_session": current_session,
        "current_semester": current_semester,
    }
    context.update(
        {
            "user_type": "Student",
            "courses": courses,
            "student": student,
            "stu":stu,
            "badges": badges,
        }
    )

    if request.GET.get("download_pdf"):
        return render_to_pdf("pdf/student_profile.html", context)

    return render(request, "lecturer/student_profile.html", context)


@login_required
@admin_required
def render_student_pdf_list(request):
    students = Student.objects.all()
    template_path = "pdf/student_list.html"
    context = {"students": students}
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="students_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f"Nous rencontrons quelques erreurs <pre>{html}</pre>")
    return response


@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    full_name = student.student.get_full_name
    student.delete()
    messages.success(request, f"l'enseignant {full_name} a été supprimé.")
    return redirect("student_list")


@login_required
@admin_required
def edit_student_program(request, pk):
    student = get_object_or_404(Student, student_id=pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProgramUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            full_name = user.get_full_name
            messages.success(request, f"{full_name}'s program has been updated.")
            return redirect("profile_single", user_id=pk)
        messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProgramUpdateForm(instance=student)
    return render(
        request,
        "accounts/edit_student_program.html",
        {"title": "Edit Program", "form": form, "student": student},
    )


# ########################################################
# Parent Views
# ########################################################


@method_decorator([login_required, admin_required], name="dispatch")
class ParentAdd(CreateView):
    model = Parent
    form_class = ParentAddForm
    template_name = "accounts/parent_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Parent ajouté avec succès.")
        return super().form_valid(form)

def save_firebase_token(request):
    if request.method == 'POST':
        token = request.POST.get('firebase_token')
        user = request.user  # Assurez-vous que l'utilisateur est authentifié
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.firebase_token = token
        user_profile.save()
        return JsonResponse({"status": "success", "message": "Token enregistré avec succès."})
    return JsonResponse({"status": "error", "message": "Requête invalide."}, status=400)

def send_notification(request):
    if request.method == 'POST':
        user = request.user  # Utilisateur authentifié
        user_profile = UserProfile.objects.get(user=user)
        token = user_profile.firebase_token

        if token:
            title = "Nouveau message"
            body = "Vous avez reçu un nouveau message."
            response = send_push_notification(token, title, body)
            return JsonResponse({"status": "success", "response": response})
        else:
            return JsonResponse({"status": "error", "message": "Aucun token Firebase trouvé."}, status=400)
    return JsonResponse({"status": "error", "message": "Requête invalide."}, status=400)