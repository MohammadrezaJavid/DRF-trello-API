from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    PRIVATE = 'pr'
    PUBLIC = 'pu'

    VISIBILITY_TYPES = (
        (PRIVATE, 'private'),
        (PUBLIC, 'public'),
    )

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="title")
    visibility = models.CharField(max_length=2, choices=VISIBILITY_TYPES, default=PRIVATE)
    creator = models.ForeignKey(User, related_name="boards", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class List(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="title")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    boardId = models.IntegerField(editable=False, validators=[MinValueValidator(1)])
    createdAt = models.DateTimeField(auto_now_add=True)

