from rest_framework import serializers
from api.models import FriendRequest, User
from django.contrib.auth import authenticate
import logging


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#         user = authenticate(username=email, password=password)
#         if not user:
#             logging.error(f"Authentication failed for email: {email}")
#             raise serializers.ValidationError("Invalid login credentials")
#         data['user'] = user
#         return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)  # Ensure this uses email as username
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        data['user'] = user
        return data


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'  # You can also specify the fields explicitly
