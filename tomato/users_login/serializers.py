# Django Rest Framework
from rest_framework import serializers

# users_login
from .models import UserProfile


class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializa objeto de perfil de usuario """

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'name', 'last_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validated_data):
        """ Create and return a new user """
        user = UserProfile.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        """ Update a user """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)
