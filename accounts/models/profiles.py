from django.utils.translation import gettext_lazy as _
from django.db import models



class BaseProfile(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to="profile/",default="profile/default.png")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def get_fullname(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return  self.user.email
    
    def __str__(self):
        return self.get_fullname if self.first_name and self.last_name else self.user.email
    
    class Meta:
        abstract = True
    

class UserProfile(BaseProfile):
    # relation fields
    user = models.OneToOneField('User', on_delete=models.CASCADE,related_name="profile")


class SellerUserProfile(BaseProfile):
    # relation fields
    user = models.OneToOneField('User', on_delete=models.CASCADE,related_name="seller_profile")

    # primary key fields
    phone_number = models.CharField(max_length=12, unique=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, null=True)

    # permission fields
    status = models.BooleanField(default=False)

    
    # info fields
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    

class Shop(models.Model):
    seller = models.ForeignKey(SellerUserProfile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, unique=True)
    cell_phone = models.CharField(max_length=12, unique=True)


    def __str__(self):
        return f"{self.name}"
