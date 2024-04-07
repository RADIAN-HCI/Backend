from rest_framework import viewsets
from course.serializers import CourseSerializer
from .models import Course
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     course = serializer.save()
    #     user = self.request.user
    #     user.courses.add(course)

    # def perform_update(self, serializer):
    #     course = serializer.save()
    #     user = self.request.user
    #     user.courses.add(course)
