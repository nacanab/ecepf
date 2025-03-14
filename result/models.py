from decimal import Decimal
from django.conf import settings

from django.db import models
from django.urls import reverse

from accounts.models import Student
from core.models import Semester
from course.models import Course



class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="taken_courses"
    )

