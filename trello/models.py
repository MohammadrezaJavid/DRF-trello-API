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
    assignUsers = models.ManyToManyField(User, related_name="assignBoards", blank=True)


class List(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="title")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    boardId = models.IntegerField(editable=False, validators=[MinValueValidator(1)])
    creator = models.ForeignKey(User, related_name="lists", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    WATCH = 'w'
    NOT_WATCH = 'nw'

    NOTIFICATIONS_STATUS = (
        (WATCH, 'w'),
        (NOT_WATCH, 'nw'),
    )

    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="title")
    createdAt = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, verbose_name="description")
    tag = models.CharField(max_length=150, verbose_name="tag")
    notificationsStatus = models.CharField(max_length=2, choices=NOTIFICATIONS_STATUS, default=NOT_WATCH)

    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="cards")
    listId = models.IntegerField(editable=False, validators=[MinValueValidator(1)])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cardsCreate")
    assignUsers = models.ManyToManyField(User, related_name="assignCards", blank=True)
    deadLine = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="deadLine")

    def __str__(self):
        return 'cardId: ' + str(self.id) + ' | ' + 'listId:' + str(self.listId) + ' | ' + str(self.creator)


class Notification(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    message = models.CharField(max_length=300, verbose_name="notification message")
    createdAt = models.DateTimeField(auto_now_add=True)

    notificationCard = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="notificationsCard",
        blank=True
    )
    # on_delete CASCADE for user, yes or no ??
    notificationUsers = models.ManyToManyField(User, related_name="notificationsUser", blank=True)
    REQUIRED_FIELDS = ["message"]


class Comment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    text = models.CharField(max_length=300)
    writedAt = models.DateTimeField(auto_now_add=True)

    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writerComments")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    cardId = models.IntegerField(editable=False, null=True, blank=True, validators=[MinValueValidator(1)])
    replyComment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", blank=True, null=True)
    replyCommentId = models.IntegerField(editable=False, null=True, blank=True, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['-writedAt']
