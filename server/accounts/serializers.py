from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
             raise serializers.ValidationError({"error": "Email is not verified. Please verify your email first."})
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'phone',
            'address',
            'dob',
            'is_verified',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    secret_key = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "secret_key",
        ]

    def validate(self, attrs):
        role = attrs.get('role', 'customer')
        secret_key = attrs.get('secret_key')
        
        from django.conf import settings
        if role in ['admin', 'surveyor']:
            if secret_key != settings.REGISTER_SECRET_KEY:
                raise serializers.ValidationError({"secret_key": f"A valid secret key is required to register as {role}."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('secret_key', None)
        user = User.objects.create_user(**validated_data)
        return user

