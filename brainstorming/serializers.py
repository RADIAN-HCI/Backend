from rest_framework import serializers
from .models import BrainStorm

# from core.serializers import UserProfileSerializer
# from assignment.serializers import AssignmentSerializer
# from course.serializers import CourseSerializer


class BrainStormSerializer(serializers.ModelSerializer):
    # owner = UserProfileSerializer()
    # assignment = AssignmentSerializer()
    # course = CourseSerializer()
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BrainStorm
        fields = "__all__"
        # fields = ["id", "created_at", "course", "assignment", "owner", "prompt"]
