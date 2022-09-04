from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):
    """Вход только для админа."""
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and request.user.is_admin)


class IsMyAdminOrReadOnly(permissions.BasePermission):
    """Вход только для чтения, редактирование только для админа."""
    def has_permission(self, request, view):
        return bool((request.method in permissions.SAFE_METHODS)
                    or (request.user.is_authenticated
                        and request.user.is_admin))


class IsStaffOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Вход только для чтения, редактирование только для админа,
    модератора или автора.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated
                    and ((request.user == obj.author)
                         or (request.user.role in (User.ADMIN, User.MODER))))
