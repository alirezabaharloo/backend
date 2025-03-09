from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from ..managers import UserManager
from utilities import permission_detector

USER_TYPES = [
    'admin',
    'seller',
    'normal'
]


class User(AbstractBaseUser, PermissionsMixin):

    # primary key fields
    email = models.EmailField(_("email address"), unique=True)

    # permission fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    # date fields
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # info fields
    increment_version = models.PositiveIntegerField(default=0)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = UserManager()

    def __str__(self):                          
        return f"{self.email} - {self.show_user_permission()}"
    


    def show_user_permission(self):
        return f"{permission_detector(admin=self.is_superuser, seller=self.is_seller)}"
    

    def get_profile_obj(self):
        try:
            return self.profile
        except Exception:
            return self.seller_profile
        
    