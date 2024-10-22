from django.urls import path
from .views import RegisterStudent,LoginStudent,StudentListAPIView,CourseListAPIView,EnrollInCourse,EnrolledCoursesAPIView

urlpatterns = [
    path("register/", RegisterStudent.as_view(), name="register"),
    path("login/", LoginStudent.as_view(), name="login"),
    path("students/", StudentListAPIView.as_view(), name="student-list"),
    path("courses/", CourseListAPIView.as_view(), name="course-list"),
    path("enroll/", EnrollInCourse.as_view(), name="enroll-course"),
    path(
        "enrolled-courses/<int:student_id>/",
        EnrolledCoursesAPIView.as_view(),
        name="enrolled-courses",
    ),
]
