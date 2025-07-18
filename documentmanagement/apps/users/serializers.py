from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        email=data.get("email")
        password=data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.user_id,
            'email': user.email,
            'full_name': user.full_name
        }
    
class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    full_name =serializers.CharField(max_length=255)

    print(email, password)
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value