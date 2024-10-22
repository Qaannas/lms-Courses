from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer,CourseSerializer
from rest_framework.views import APIView
from .models import Student,Course,Enrollment
from django.contrib.auth.hashers import check_password
from rest_framework import generics

# views.py
from rest_framework.permissions import IsAuthenticated


class RegisterStudent(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginStudent(APIView):
    def post(self, request):
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            student = Student.objects.get(name=name)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if check_password(password, student.password):
            # Get enrolled course IDs
            enrolled_courses = student.courses.values_list("id", flat=True)

            return Response(
                {
                    "message": "Login successful",
                    "name": student.name,
                    "studentId": student.id,
                    "enrolledCourses": list(
                        enrolled_courses
                    ),  # Include enrolled course IDs
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrolledCoursesAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        return Student.objects.get(id=student_id).courses.all()


class EnrollInCourse(APIView):
    def post(self, request):
        student_id = request.data.get("studentId")
        course_id = request.data.get("courseId")

        try:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)

            # Create a new Enrollment instance
            enrollment = Enrollment(student=student, course=course)
            enrollment.save()

            return Response(
                {"message": "Enrolled successfully"}, status=status.HTTP_201_CREATED
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
