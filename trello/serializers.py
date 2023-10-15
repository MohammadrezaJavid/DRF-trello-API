from django.core.validators import MinValueValidator
from rest_framework import serializers
from .models import Board, List


class BoardSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    lists = serializers.PrimaryKeyRelatedField(many=True, queryset=List.objects.all(), required=False)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'visibility', 'createdAt',
            'creator', 'lists',
        ]


class ListSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    boardId = serializers.IntegerField(write_only=True, required=True,
                                       validators=[MinValueValidator(1)])

    class Meta:
        model = List
        fields = [
            'id', 'title', 'boardId', 'createdAt',
            'board',
        ]
