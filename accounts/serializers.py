from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password
from .models import User
from trello.models import Board, Card, List, Comment


class UserSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Board.objects.all(), required=False)
    lists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=List.objects.all(), required=False)
    cardsCreate = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Card.objects.all(), required=False)
    writerComments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Comment.objects.all())
    assignBoards = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    assignCards = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'firstName', 'lastName',
            'boards', 'lists', 'cardsCreate',
            'writerComments', 'assignBoards', 'assignCards',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    # password field is write only, mandatory
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'password', 'confirmPassword')

    def validate(self, user):
        if user['password'] != user['confirmPassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return user

    def create(self, validated_data):
        user = User.objects.create_user(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
