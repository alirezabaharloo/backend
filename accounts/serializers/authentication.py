from rest_framework import serializers
from ..models import *
from ..mixins import PasswordSerializerMixin
from rest_framework_simplejwt.serializers import *




class RegisterSerializer(PasswordSerializerMixin, serializers.ModelSerializer):

    
    class Meta:
        model = User
        fields = ('email', 'password', 'password1')
    
    def create(self, validate_data):
        # delete password1 field to prevent error because we use password in create_user
        del validate_data['password1']

        # if we pass seller in context (this means a seller want to register)
        if self.context.get('seller'):
            validate_data['is_seller'] = True

        user = User.objects.create_user(**validate_data)


        return user
    


class ChangePasswordSerializer(PasswordSerializerMixin, serializers.Serializer):
    old_password = serializers.CharField()

    def __init__(self, *args ,**kwargs):

        super().__init__(*args ,**kwargs)

        self.user = self.context.get('user')

    
    def validate(self, attrs):
        user = self.user

        if not(user.check_password(attrs['old_password'])):
            raise serializers.ValidationError({'old_password': 'invalid password!'})

        return super().validate(attrs)


    def create(self, validate_data):
        user = self.user
        user.set_password(validate_data['password'])

        user.save()

        return user
    


class ResetPasswordSerializer(PasswordSerializerMixin, serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = self.context.get("request")


    def create(self, validated_data):
        user = self.request.user

        user.set_password(validated_data['password'])
        user.save()
        
        return user


