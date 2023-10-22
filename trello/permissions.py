from rest_framework import permissions
from .models import Board, List, Card, User


class IsAccessToBoard(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method == 'DELETE') or (request.method == 'PUT'):
            return self.isTrueDelete(request, view)
        elif (request.method == 'GET') and ('id' not in request.query_params):
            return True
        elif request.method == 'POST':
            return self.isTruePost(request)
        elif (request.method == 'GET') and ('id' in request.query_params):
            return self.isTrueGet(request, view)

    def isTrueGet(self, request, view):
        return (self.isTrueDelete(request, view)) or (view.get_object().visibility == 'pu') or (
                request.user in view.get_object().assignUsers)

    @staticmethod
    def isTruePost(request):
        return request.user in User.objects.all()

    @staticmethod
    def isTrueDelete(request, view):
        return request.user == view.get_object().creator

    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (obj.visibility == 'pu') or (
                request.user in obj.assignUsers)


class IsAccessToList(permissions.BasePermission):

    @staticmethod
    def isAssignBoard(request) -> bool:
        boardId = request.data.get('boardId')
        boards = Board.objects.filter(assignUsers__id=request.user.pk)
        for board in boards:
            if boardId == board.pk:
                return True
        return False

    def has_permission(self, request, view):
        if (request.method == 'DELETE') or (request.method == 'PUT'):
            return IsAccessToBoard.isTrueDelete(request, view)
        elif request.method == 'POST':
            return self.isTruePost(request)
        elif (request.method == 'GET') and ('id' in request.query_params):
            return self.isTrueGet(request, view)
        else:
            return True

    def isTrueGet(self, request, view):
        return (request.user == view.get_object().board.creator) or (
            IsAccessToBoard.isTrueDelete(request, view)) or (
                       view.get_object().board.visibility == 'pu') or (
                   self.isAssignBoard(request))

    def isTruePost(self, request):
        return (request.user == Board.objects.get(id=request.data['boardId']).creator) or (
                Board.objects.get(id=request.data['boardId']).visibility == 'pu') or (
                   self.isAssignBoard(request))

    def has_object_permission(self, request, view, obj):
        return (obj.board.creator == request.user) or (obj.board.visibility == 'pu')


class IsAccessToCard(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method == 'DELETE') or (request.method == 'PUT'):
            return IsAccessToBoard.isTrueDelete(request, view)
        elif request.method == 'POST':
            return self.isTruePost(request)
        elif (request.method == 'GET') and (type(view.kwargs.get('id')) == int):
            return self.isTrueGet(request, view.kwargs.get('id'))
        else:
            return True

    @staticmethod
    def isTrueGet(request, cardId):
        if (Card.objects.get(id=cardId).list.board.visibility == 'pu') or (Card.objects.get(
                id=cardId).creator == request.user):
            return True
        else:
            return False

    @staticmethod
    def isTruePost(request):
        return (request.user == List.objects.get(id=request.data['listId']).creator) or (
                List.objects.get(id=request.data['listId']).board.visibility == 'pu')

    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (obj.list.board.visibility == 'pu')


class IsAccessToComment(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method == 'DELETE') or (request.method == 'PUT'):
            return IsAccessToBoard.isTrueDelete(request, view)
        elif request.method == 'POST':
            return self.isTruePost(request)
        elif (request.method == 'GET') and ('id' in request.query_params):
            return self.isTrueGet(request, view)
        else:
            return True

    @staticmethod
    def isTrueGet(request, view):
        return (request.user == view.get_object().writer) or (
                view.get_object().card.list.board.visibility == 'pu')

    @staticmethod
    def isTruePost(request):
        return (request.user == Card.objects.get(id=request.data['cardId']).creator) or (
                Card.objects.get(id=request.data['cardId']).list.board.visibility == 'pu')
