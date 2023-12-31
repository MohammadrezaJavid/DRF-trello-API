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
from accounts.models import User


class BoardView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsAccessToBoard,)
    queryset = models.Board.objects.all()
    serializer_class = serializers.BoardSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        querysetAssignUser = models.Board.objects.filter(assignUsers__id=self.request.user.pk)
        querysetPublic = models.Board.objects.filter(visibility='pu')
        querysetCreator = models.Board.objects.filter(creator=self.request.user.pk)
        queryset = querysetPublic | querysetCreator | querysetAssignUser

        return queryset.distinct()

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

    def list(self, request, *args, **kwargs):
        querysetAssignUser = models.Card.objects.filter(assignUsers__id=self.request.user.pk)
        querysetCreator = models.Card.objects.filter(creator=self.request.user.pk)
        querysetPublic = models.Card.objects.all()

        queryset = querysetCreator | querysetAssignUser | querysetPublic
        queryset = queryset.distinct()

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        ID = int(self.request.data['listId'])
        emails = self.request.data['assignUsers']
        
        assign_user_id_list = []
        
        for email in emails:
            try:
                user = User.objects.get(email=email)
                assign_user_id_list.append(user.id)
            except User.DoesNotExist:
                assert("user not found")
        
        try:
            lists = models.List.objects.get(id=ID)
            serializer.save(list=lists, creator=self.request.user, assignUsers=assign_user_id_list)
        except models.List.DoesNotExist:
            raise RuntimeWarning("List Object is None")


class TagCardView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Card.objects.all()
    serializer_class = serializers.TagCardSerializer

    def list(self, request, *args, **kwargs):
        tag = self.kwargs.get('tag')
        queryset = self.filter_queryset(self.get_queryset().filter(tag=tag, creator=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        queryset = models.Notification.objects.filter(notificationUsers__id=self.request.user.pk)
        return queryset


class CommentView(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = (IsAccessToComment,)
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
