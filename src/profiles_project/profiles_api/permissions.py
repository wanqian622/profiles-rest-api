from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile. """

    # has_object_permission function return a true or false
    # depending on what the result of the permission is.
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""

        # Allow users to be able to view any profile in the system
        # By checking the safe methods list which is provided by 
        # the django rest framework.
        # A safe method is a HTTP method that is classified as safe.
        # It is a non destructive method so it allows you to retrieve
        # data but it does not allow you to change or modify or delete
        # any objects in the system.
        # A safe method is HTTP GET.
        if request.method in permissions.SAFE_METHODS:
            return True


        # If the users updates their own profile
        return obj.id == request.user.id
