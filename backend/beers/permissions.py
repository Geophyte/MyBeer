from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_staff):
            return True
        return obj.author == request.user
