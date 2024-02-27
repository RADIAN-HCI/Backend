from rest_framework import serializers
from .models import User, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'created_at', 'username', 'role', 'courses']
