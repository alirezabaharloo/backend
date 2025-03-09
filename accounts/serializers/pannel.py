from rest_framework import serializers
from ..models import *
from rest_framework_simplejwt.serializers import *

class BaseProfileSerializerMixin(serializers.Serializer):
    email = serializers.SerializerMethodField()
    user_perms = serializers.SerializerMethodField()

    def get_user_perms(self, obj: SellerUserProfile):
        return f"{obj.user.show_user_permission()}"

    def get_email(self, obj):
        return f"{obj.user.email}"


class ProfileSerializer(BaseProfileSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "phone_number", "image", "email", "user_perms")


    def get_user_perms(self, obj: SellerUserProfile):
        return f"{obj.user.show_user_permission()}"


class SellerProfileSerializer(BaseProfileSerializerMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    national_code = serializers.CharField(required=True)


    class Meta:
        model = SellerUserProfile
        fields=  ("first_name", "last_name", "phone_number", "national_code", "image", "email", "user_perms")


    def validate_phone_number(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("invalid phone_number!")
        
        return value
    
    def validate_national_code(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("invalid national_code!")
        
        return value



class SellerListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )

    class Meta:
        model = SellerUserProfile
        fields = ['user', 'phone_number', 'first_name', 'last_name', 'status']


class ShopSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")


    class Meta:
        model = Shop
        fields = ['name', 'cell_phone']

    def validate(self, validate_data):
        if Shop.objects.filter(seller=self.request.user.seller_profile).exists():
            raise serializers.ValidationError("shop with this seller already exists!")
        
        return validate_data
    
    def create(self, validated_data):
        shop = Shop.objects.create(name=validated_data['name'], cell_phone=validated_data['cell_phone'], seller=self.request.user)
        return shop
    

    
# class UserListSerializer(serializers.ModelSerializer):
#     perms = serializers.SerializerMethodField()
#     rofile_url = serializers.HyperlinkedRelatedField(
#         view_name="profile",
#         lookup_field="seller_profile",
#     )  


#     class Meta:
#         model = User
#         fields = ("email", "perms", "rofile_url")


#     def get_perms(self, obj):
#         return f"{obj.show_user_permission()}"


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("email", "url", "id")