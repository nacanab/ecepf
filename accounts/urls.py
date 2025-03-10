from django.urls import path, include

# from django.contrib.auth.views import (
#     PasswordResetView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView,
#     LoginView,
#     LogoutView,
# )
from .views import (
    desasign_student,
    profile,
    profile_single,
    admin_panel,
    profile_update,
    change_password,
    LecturerFilterView,
    StudentListView,
    staff_add_view,
    edit_staff,
    delete_staff,
    student_add_view,
    edit_student,
    delete_student,
    edit_student_program,
    ParentAdd,
    student_single,
    validate_username,
    register,
    render_lecturer_pdf_list,  # new
    render_student_pdf_list,  # new
    child_profile,
    accueil,
    choose_role,
    assign_students,
    student_list,
    lecturer_assign_list,
    save_firebase_token
    )

# from .forms import EmailValidationOnForgotPassword


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("chat/", include('chat.urls')),
    path("admin_panel/", admin_panel, name="admin_panel"),
    path("profile/", profile, name="profile"),
    path('child_profile/', child_profile, name='child_profile'),
    path("profile/<int:user_id>/detail/", profile_single, name="profile_single"),
    path("setting/", profile_update, name="edit_profile"),
    path("change_password/", change_password, name="change_password"),
    path("lecturers/", LecturerFilterView.as_view(), name="lecturer_list"),
    path("lecturer/add/", staff_add_view, name="add_lecturer"),
    path("staff/<int:pk>/edit/", edit_staff, name="staff_edit"),
    path("lecturers/<int:pk>/delete/", delete_staff, name="lecturer_delete"),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("student/add/", student_add_view, name="add_student"),
    path("student/<int:pk>/edit/", edit_student, name="student_edit"),
    path("students/<int:pk>/delete/", delete_student, name="student_delete"),
    path(
        "edit_student_program/<int:pk>/",
        edit_student_program,
        name="student_program_edit",
    ),
    path("lecturers_assignments/",lecturer_assign_list, name="lecturer_assign_list"),
    path("assign_students/<int:lecturer_id>/", assign_students, name="assign_students"),
    path("desasign_students/<int:lecturer_id>/<int:student_id>/", desasign_student, name="desasign_students"),
    path("students_list/<int:lecturer_id>", student_list, name="lecturer_student_list"),
    path("profil_etudiant/<int:user_id>",student_single,name="profil_etudiant"),
    path("parents/add/", ParentAdd.as_view(), name="add_parent"),
    path("ajax/validate-username/", validate_username, name="validate_username"),
    path("register/choose_role", choose_role, name="role"),
    path("register/<str:role>", register, name="register"),
    # paths to pdf
    path(
        "create_lecturers_pdf_list/", render_lecturer_pdf_list, name="lecturer_list_pdf"
    ),  # new
    path(
        "create_students_pdf_list/", render_student_pdf_list, name="student_list_pdf"
    ),
    path('save-firebase-token/',save_firebase_token,name='save_firebase_token')
]
