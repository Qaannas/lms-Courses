from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer
from rest_framework.views import APIView
from .models import Student, Course, Enrollment
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from django.http import JsonResponse

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
            enrolled_courses = Enrollment.objects.filter(student=student).values_list("course_id", flat=True)
            
            return Response(
                {
                    "message": "Login successful",
                    "name": student.name,
                    "studentId": student.id,
                    "enrolledCourses": list(enrolled_courses),
                    
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
        rating = request.data.get("rating", None)

        try:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)

            # Check if enrollment with rating already exists
            enrollment, created = Enrollment.objects.get_or_create(
                student=student, course=course
            )

            if enrollment.rating is not None:
                return Response(
                    {
                        "message": "Already enrolled with a rating",
                        "rating": enrollment.rating,
                    },
                    status=status.HTTP_200_OK,
                )

            # Save new rating if provided
            if rating:
                enrollment.rating = rating
                enrollment.save()

            return Response(
                {"message": "Enrolled successfully", "rating": enrollment.rating},
                status=status.HTTP_201_CREATED,
            )
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateEnrollmentRating(APIView):
    def post(self, request):
        student_id = request.data.get("studentId")
        course_id = request.data.get("courseId")
        rating = request.data.get("rating")

        try:
            enrollment = Enrollment.objects.get(
                student_id=student_id, course_id=course_id
            )
            enrollment.rating = rating
            enrollment.save()

            return Response(
                {"message": "Rating submitted successfully"}, status=status.HTTP_200_OK
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubmitRatingView(APIView):
    def post(self, request, student_id, course_id):
        rating = request.data.get("rating")

        try:
            # Fetch the enrollment record
            enrollment = Enrollment.objects.get(
                student_id=student_id, course_id=course_id
            )
            # Update rating
            enrollment.rating = rating
            enrollment.save()
            return JsonResponse(
                {"success": True, "message": "Rating saved successfully!"}
            )
        except Enrollment.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Enrollment not found."}, status=404
            )


# views.py
class EnrollmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        serializer.save(
            student_id=self.request.data["student_id"],
            course_id=self.request.data["course_id"],
        )


class EnrollmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
