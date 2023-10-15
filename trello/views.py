from rest_framework import viewsets
from . import models, serializers
from .permissions import IsOwnerOnlyOrPublic, IsAccessToList


class BoardView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsOwnerOnlyOrPublic,)
    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        querysetPublic = models.Board.objects.filter(visibility='pu')
        querysetCreator = models.Board.objects.filter(creator=self.request.user)
        queryset = querysetPublic | querysetCreator

        return queryset


class ListView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsAccessToList,)
    queryset = models.List.objects.all()
    serializer_class = serializers.ListSerializer

    def perform_create(self, serializer):
        ID = int(self.request.data['boardId'])
        try:
            board = models.Board.objects.get(id=ID)
            serializer.save(board=board)
        except models.Board.DoesNotExist:
            raise RuntimeWarning("Board Object is None")
