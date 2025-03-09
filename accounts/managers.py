from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .models import SellerUserProfile, UserProfile


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()

        # create profile (if create_selleruser called, SellerUserProfile table will create, otherwise NormalUserProfile)
        if extra_fields.get("is_seller"):
            SellerUserProfile.objects.create(user=user)
        
        else:
            UserProfile.objects.create(user=user) 

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_seller", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(email, password, **extra_fields)
    

    def create_selleruser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_seller", True)
        
        if extra_fields.get('is_seller') is not True:
            raise ValueError(_("seller user must have is_seller=True"))

        return self.create_user(email, password, **extra_fields)