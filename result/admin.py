from django.contrib import admin
from django.contrib.auth.models import Group

from .models import TakenCourse


class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "course",
    ]


admin.site.register(TakenCourse, ScoreAdmin)
