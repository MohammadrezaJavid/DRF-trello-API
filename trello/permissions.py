from rest_framework import permissions


class IsOwnerOnlyOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.creator == request.user) or (obj.visibility == 'pu')


class IsAccessToList(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.board.creator == request.user) or (obj.board.visibility == 'pu')
