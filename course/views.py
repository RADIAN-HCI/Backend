from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from course.serializers import CourseSerializer
from .models import Course
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def add_course(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if course in user.courses.all():
            return Response(
                {"message": "Course already in user's profile"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.courses.add(course)
        return Response(
            {"message": "Course added successfully"}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def remove_course(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if course not in user.courses.all():
            return Response(
                {"message": "Course not found in user's profile"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.courses.remove(course)
        return Response({"message": "Course removed successfully"})
