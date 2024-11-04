from rest_framework import serializers
from .models import Student,Course,Enrollment
from django.contrib.auth.hashers import make_password,check_password
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        name = data.get("name")
        password = data.get("password")

        try:
            student = Student.objects.get(name=name)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Manually check the password using `check_password`
        if not check_password(password, student.password):
            raise serializers.ValidationError("Invalid credentials")

        return {
            "name": student.name,
            "studentId": student.id,  # Return the studentId as well
        }


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "price"]


class StudentSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["name", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# serializers.py
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrollment_date", "rating"]
