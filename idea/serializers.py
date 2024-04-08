from rest_framework import serializers
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = "__all__"
        # fields = ['id', 'created_at', 'title', 'details', 'difficulty', 'innovation', 'brainstorm']
