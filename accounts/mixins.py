from rest_framework import serializers



class PasswordSerializerMixin(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    
    def validate(self, attrs):

        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({'password': 'passwords must be the same!'})
        
        return attrs
