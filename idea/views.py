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

    def get_queryset(self):
        queryset = Idea.objects.all()
        # Support nested route /brainstorms/{brainstorm_pk}/ideas and query param brainstorm_id
        brainstorm_param = self.kwargs.get('brainstorm_pk') or self.request.query_params.get('brainstorm_id') or self.request.query_params.get('brainstorm')

        if brainstorm_param:
            try:
                brainstorm_id = int(brainstorm_param)
            except (TypeError, ValueError):
                return queryset.none()

            queryset = queryset.filter(brainstorm_id=brainstorm_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
