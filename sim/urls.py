from django.urls import path
from .views import RegisterStudent,LoginStudent,StudentListAPIView,CourseListAPIView,EnrollInCourse,EnrolledCoursesAPIView,SubmitRatingView,UpdateEnrollmentRating

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
    path(
        "enroll/<int:student_id>/<int:course_id>/",
        SubmitRatingView.as_view(),
        name="submit-rating",
    ),
    path(
        "enroll/update-rating/",  # Add this path for updating ratings
        UpdateEnrollmentRating.as_view(),
        name="update-enrollment-rating",
    ),
    
]
