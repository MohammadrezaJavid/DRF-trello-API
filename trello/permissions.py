from rest_framework import permissions
from .models import Board, List


class IsAccessToBoard(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user == view.get_object().creator
        elif (request.method == 'POST') or (request.method == 'PUT') or (
                (request.method == 'GET') and ('id' not in request.query_params)):
            return True
        elif (request.method == 'GET') and ('id' in request.query_params):
            return (request.user == view.get_object().creator) or \
                   (view.get_object().visibility == 'pu')

    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (obj.visibility == 'pu')


class IsAccessToList(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user == view.get_object().creator
        elif (request.method == 'POST') or (request.method == 'PUT'):
            return (request.user == Board.objects.get(id=request.data['boardId']).creator) or (
                    Board.objects.get(id=request.data['boardId']).visibility == 'pu')
        elif (request.method == 'GET') and ('id' in request.query_params):
            return (request.user == view.get_object().board.creator) or (
                    request.user == view.get_object().creator) or (
                           view.get_object().board.visibility == 'pu')
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return (obj.board.creator == request.user) or (obj.board.visibility == 'pu')


class IsAccessToCard(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user == view.get_object().creator
        elif (request.method == 'POST') or (request.method == 'PUT'):
            return (request.user == List.objects.get(id=request.data['listId']).creator) or (
                    List.objects.get(id=request.data['listId']).board.visibility == 'pu')
        elif (request.method == 'GET') and ('id' in request.query_params):
            return (request.user == view.get_object().creator) or (
                    view.get_object().list.board.visibility == 'pu')
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (obj.list.board.visibility == 'pu')
