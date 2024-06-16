from rest_framework import permissions


class UserAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or \
            request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or \
            request.user.is_staff or obj.owner == request.user


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS \
            or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS \
            or request.user.is_staff
