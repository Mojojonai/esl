from rest_framework import viewsets, permissions
from .models import GameTemplate
from .serializers import GameTemplateSerializer


class GameTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for game templates."""
    queryset = GameTemplate.objects.all()
    serializer_class = GameTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
