from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if 'Admin' in request.user.groups.all().values_list('name', flat=True):
            return True
        else:
            return obj.is_owner(request.user)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'Admin' in request.user.groups.all().values_list('name', flat=True)


class IsVerified(permissions.BasePermission):
    message = 'You do not have permission. Please contact an admin and get your account verified'

    def has_permission(self, request, view):
        return request.user.verified
