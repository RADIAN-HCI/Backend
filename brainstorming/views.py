from rest_framework import viewsets
from .models import BrainStorm
from .serializers import BrainStormSerializer
from rest_framework.permissions import IsAuthenticated


class BrainstormViewSet(viewsets.ModelViewSet):
    queryset = BrainStorm.objects.all()
    serializer_class = BrainStormSerializer
    permission_classes = [IsAuthenticated]
