from rest_framework import viewsets
from . import models, serializers
from .permissions import IsOwnerOnly


class BoardView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsOwnerOnly,)
    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        visibility = self.request.query_params.get('visibility', 'public')
        queryset = models.Board.objects.filter(visibility=visibility)
        if visibility == 'private':
            queryset = queryset.filter(creator=user)
        return queryset
