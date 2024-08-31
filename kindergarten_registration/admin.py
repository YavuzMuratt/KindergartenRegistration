# admin.py
from django.contrib import admin
from .models import Student, Kindergarten, Class


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'disqualified', 'assigned_class')
    readonly_fields = ('registration_date', 'points', 'disqualified')


@admin.register(Kindergarten)
class KindergartenAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_limit', 'num_classes')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('kindergarten', 'limit')
