from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'created_at', 'assignment', 'title', 'details_original', 'details_modified', 'author', 'attachment']
