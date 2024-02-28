# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ViewSet):
    def partial_update(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Question does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
