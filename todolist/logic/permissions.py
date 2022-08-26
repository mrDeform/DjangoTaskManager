from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.manager == request.user:
            return True
        return bool(request.user and request.user.is_staff)


class IsAdminOrManagerOrResponsible(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.task.manager or request.user == obj.responsible:
            return True
        return bool(request.user and request.user.is_staff)