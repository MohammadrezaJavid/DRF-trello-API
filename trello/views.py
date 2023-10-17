from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models, serializers
from .permissions import (
    IsAccessToBoard,
    IsAccessToList,
    IsAccessToCard,
    IsAccessToComment
)


class BoardView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsAccessToBoard,)
    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        querysetPublic = models.Board.objects.filter(visibility='pu')
        querysetCreator = models.Board.objects.filter(creator=self.request.user.pk)
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
            serializer.save(board=board, creator=self.request.user)
        except models.Board.DoesNotExist:
            raise RuntimeWarning("Board Object is None")


class CardView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsAccessToCard,)
    queryset = models.Card.objects.all()
    serializer_class = serializers.CardSerializer

    def perform_create(self, serializer):
        ID = int(self.request.data['listId'])
        try:
            lists = models.List.objects.get(id=ID)
            serializer.save(list=lists, creator=self.request.user)
        except models.List.DoesNotExist:
            raise RuntimeWarning("List Object is None")


class TagCardView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Card.objects.all()
    serializer_class = serializers.TagCardSerializer

    def list(self, request, *args, **kwargs):
        tag = self.kwargs.get('tag')
        queryset = self.filter_queryset(self.get_queryset().filter(tag=tag, creator=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = [IsAccessToComment]
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        try:
            if 'replyCommentId' in self.request.data:
                cardId = int(self.request.data['cardId'])
                card = models.Card.objects.get(id=cardId)

                replyCommentId = int(self.request.data['replyCommentId'])
                replyComment = models.Comment.objects.get(id=replyCommentId)

                serializer.save(card=card, writer=self.request.user, replyComment=replyComment)
            else:
                cardId = int(self.request.data['cardId'])
                card = models.Card.objects.get(id=cardId)
                serializer.save(card=card, writer=self.request.user)

        except models.Card.DoesNotExist:
            raise RuntimeWarning("Card Object is None")
