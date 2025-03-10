from django.contrib import admin
from .models import Badge, AttributionBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'image', 'description')

@admin.register(AttributionBadge)
class AttributionBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'date_attribution')

# Register your models here.
