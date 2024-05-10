from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Idea
from .serializers import IdeaSerializer
from rest_framework.permissions import IsAuthenticated

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        brainstorm = request.query_params.get('brainstorm_id')

        if not brainstorm:
            return Response({"error": "Brainstorm ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            brainstorm = int(brainstorm)
        except ValueError:
            return Response({"error": "Brainstorm ID must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        print(brainstorm)
        try:
            ideas = Idea.objects.filter(brainstorm=brainstorm)
            serializer = self.get_serializer(ideas, many=True)
            return Response(serializer.data)
        except Idea.DoesNotExist:
            return Response({"error": "Ideas not found for the specified brainstorm"}, status=status.HTTP_404_NOT_FOUND)
