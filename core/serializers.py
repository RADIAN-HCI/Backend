# from rest_framework import serializers
# from .models import User, Course


# class UserProfileSerializer(serializers.ModelSerializer):
#     # courses = CourseSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         # fields = ['id', 'username', 'password', 'courses']
#         fields = ["id", "username"]


from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)

from course.serializers import CourseSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "first_name", "last_name"]


class UserSerializer(BaseUserSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "first_name", "last_name", "courses"]
