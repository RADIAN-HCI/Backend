from .models import Idea
from rest_framework import viewsets
from .serializers import IdeaSerializer
from rest_framework.permissions import IsAuthenticated


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
