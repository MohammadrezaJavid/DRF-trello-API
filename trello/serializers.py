from django.core.validators import MinValueValidator
from rest_framework import serializers
from .models import Board, List, Card, Comment, Notification
from accounts.models import User
from accounts.serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)
    lists = serializers.PrimaryKeyRelatedField(many=True, queryset=List.objects.all(), required=False)
    assignUsers = UserSerializer(many=True, required=False)
    
    class Meta:
        model = Board
        fields = [
            'id', 'title', 'visibility', 'createdAt',
            'creator', 'lists', 'assignUsers',
        ]
        extra_kwargs = {
            'assignUsers': {'required': False},
        }
        read_only_fields = ('id', 'createdAt', 'creator')

class ListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)
    board = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    boardId = serializers.IntegerField(write_only=True, required=True, validators=[MinValueValidator(1)])
    cards = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all(), required=False)

    class Meta:
        model = List
        fields = [
            'id', 'title', 'boardId', 'createdAt', 'creator',
            'board', 'cards',
        ]
        read_only_fields = ('id', 'createdAt', 'creator')

class NotificationSerializer(serializers.ModelSerializer):
    notificationUsers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Notification
        fields = ['message', 'notificationUsers']

class CommentSerializer(serializers.ModelSerializer):
    writer = UserSerializer(many=False, read_only=True)
    card = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    cardId = serializers.IntegerField(write_only=True, required=True, validators=[MinValueValidator(1)])
    replyComment = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    replyCommentId = serializers.IntegerField(write_only=True, required=False, validators=[MinValueValidator(1)])

    class Meta:
        model = Comment
        fields = [
            'text', 'writedAt',
            'writer', 'card', 'cardId', 'replyComment', 'replyCommentId',
        ]
        extra_kwargs = {
            'replyCommentId': {'required': False},
        }
        read_only_fields = ('writedAt', 'writer')

class CardSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)
    list = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    listId = serializers.IntegerField(write_only=True, required=True, validators=[MinValueValidator(1)])
    comments = CommentSerializer(many=True, required=False)
    assignUsers = serializers.SlugRelatedField(many=True, slug_field='email', queryset=User.objects.all(), required=False)
    # assignUsers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    # assignUsers = serializers(many=True, required=False)
    notificationsCard = serializers.PrimaryKeyRelatedField(many=True, queryset=Notification.objects.all(), required=False)

    class Meta:
        model = Card
        fields = [
            'id', 'title', 'createdAt', 'description', 'tag', 'notificationsStatus', 'deadLine',
            'list', 'listId', 'creator', 'comments', 'assignUsers', 'notificationsCard',
        ]
        extra_kwargs = {
            'description': {'required': False},
            'tag': {'required': False},
            'notificationsStatus': {'required': False},
            'comments': {'required': False},
            'assignUsers': {'required': False},
            'notificationsCard': {'required': False},
            'deadLine': {'required': False},
        }
        read_only_fields = ('id', 'createdAt', 'creator')

class TagCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
