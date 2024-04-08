from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
