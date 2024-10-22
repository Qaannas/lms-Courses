# sim/admin.py
from django.contrib import admin
from .models import Student ,Course,Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]  # Fields you want to display in the admin

admin.site.register(Course)
admin.site.register(Enrollment)

