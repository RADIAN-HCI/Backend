from rest_framework import serializers
from .models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'created_at', 'course', 'title', 'assignment_type']
