from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    details_modified = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        # fields = ['id', 'created_at', 'assignment', 'title', 'details_original', 'details_modified', 'author', 'attachment', 'is_selected_for_assignment', 'order']
        fields = "__all__"
