from rest_framework.permissions import BasePermission
from rest_framework import status

class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    

class IsSellerUser(BasePermission):
    """
    Allows access only to seller users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_seller
    

class IssellerUser(BasePermission):
    """
    Allows access only seller users.
    """

class IsSellerUserWithPerm(BasePermission):
    """
    Allows access only sellers with status=True.
    """
    message = "please wait for the admin ceredintials!"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_seller and 
            request.user.seller_profile.status
        )