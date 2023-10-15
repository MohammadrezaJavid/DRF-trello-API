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
        querysetPublic = models.Board.objects.filter(visibility='pu')
        querysetCreator = models.Board.objects.filter(creator=user)
        queryset = querysetPublic.union(querysetCreator)

        return queryset
