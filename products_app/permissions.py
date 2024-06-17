"""Permission classes."""

from rest_framework import permissions


class UserAdminPermission(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users to perform unsafe actions.

    Additionally, it allows only the owner of an object
    or a staff member to perform unsafe actions on that object.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the request.

        SAFE_METHODS are allowed for any user.
        Other methods require the user to be authenticated.

        Args:
            request: The current request instance.
            view: The current view instance.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, objct):
        """
        Check if the user has permission to perform the request on a specific object.

        SAFE_METHODS are allowed for any user.
        Other methods require the user to be a staff member or the owner of the object.

        Args:
            request: The current request instance.
            view: The current view instance.
            objct: The object being accessed.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        is_safe = request.method in permissions.SAFE_METHODS
        return is_safe or request.user.is_staff or objct.owner == request.user


class AdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only staff members to perform unsafe actions.

    SAFE_METHODS are allowed for any user.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the request.

        SAFE_METHODS are allowed for any user.
        Other methods require the user to be a staff member.

        Args:
            request: The current request instance.
            view: The current view instance.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        is_safe = request.method in permissions.SAFE_METHODS
        return is_safe or request.user.is_staff

    def has_object_permission(self, request, view, objct):
        """
        Check if the user has permission to perform the request on a specific object.

        SAFE_METHODS are allowed for any user.
        Other methods require the user to be a staff member.

        Args:
            request: The current request instance.
            view: The current view instance.
            objct: The object being accessed.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        is_safe = request.method in permissions.SAFE_METHODS
        return is_safe or request.user.is_staff
