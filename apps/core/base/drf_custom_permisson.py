from rest_framework import permissions


class AuthenticatedStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `staff` to do Post, Patch.
        return request.user.is_staff
