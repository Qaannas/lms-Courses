# sim/admin.py
from django.contrib import admin
from .models import Student ,Course,Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id","name", "email"]  # Fields you want to display in the admin


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


admin.site.register(Enrollment)
