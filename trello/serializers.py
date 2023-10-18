from django.core.validators import MinValueValidator
from rest_framework import serializers
from .models import Board, List, Card, Comment
from accounts.models import User


class BoardSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    lists = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=List.objects.all(),
        required=False)
    # assignUsers = UserSerializer(many=True)
    assignUsers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'visibility', 'createdAt',
            'creator', 'lists', 'assignUsers',
        ]

        extra_kwargs = {
            'assignUsers': {'required': False},
        }


class ListSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    board = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    boardId = serializers.IntegerField(
        write_only=True, required=True, validators=[MinValueValidator(1)])
    cards = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Card.objects.all(), required=False)

    class Meta:
        model = List
        fields = [
            'id', 'title', 'boardId', 'createdAt', 'creator',
            'board', 'cards',
        ]


class CardSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    list = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    listId = serializers.IntegerField(
        write_only=True, required=True, validators=[MinValueValidator(1)])
    comments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Comment.objects.all(), required=False)

    assignUsers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False)

    # assignUsers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            'id', 'title', 'createdAt', 'description', 'tag', 'notifications',
            'list', 'listId', 'creator', 'comments', 'assignUsers',
        ]

        extra_kwargs = {
            'description': {'required': False},
            'tag': {'required': False},
            'notifications': {'required': False},
            'comments': {'required': False},
            'assignUsers': {'required': False},
        }


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    card = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    cardId = serializers.IntegerField(
        write_only=True, required=True, validators=[MinValueValidator(1)])

    replyComment = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    replyCommentId = serializers.IntegerField(write_only=True, required=False, validators=[MinValueValidator(1)])

    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'writedAt',
            'writer', 'card', 'cardId', 'replyComment', 'replyCommentId',
        ]

        extra_kwargs = {
            'replyCommentId': {'required': False},
        }


class TagCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
