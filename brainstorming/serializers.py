from rest_framework import serializers
from .models import BrainStorm
from user.serializers import UserProfileSerializer
from assignment.serializers import AssignmentSerializer
from user.serializers import CourseSerializer

class BrainStormSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    assignment = AssignmentSerializer()
    course = CourseSerializer()

    class Meta:
        model = BrainStorm
        fields = ['id', 'created_at', 'course', 'assignment', 'owner', 'prompt']
