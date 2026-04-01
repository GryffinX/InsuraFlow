from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
             raise serializers.ValidationError("Email is not verified. Please verify your email first.")
        return data

class UserSerializer(serializers.ModelSerializer):
    formatted_id = serializers.SerializerMethodField()
    
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
            'formatted_id',
        ]

    def get_formatted_id(self, obj):
        prefix = {
            'customer': 'CUST',
            'agent': 'AGENT',
            'surveyor': 'SURV',
            'provider': 'PROV',
            'admin': 'ADMN'
        }.get(obj.role, 'USER')
        return f"{prefix}-{obj.id}"

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
            "phone",
            "address",
            "dob",
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
        
        # Auto-create corresponding profiles
        from insurance.models import Provider, Agent, Surveyor
        try:
            if user.role == 'provider':
                Provider.objects.get_or_create(user=user, defaults={'company_name': user.username, 'contact_email': user.email})
            elif user.role == 'agent':
                Agent.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email})
            elif user.role == 'surveyor':
                Surveyor.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email, 'license_no': f"LNC-{user.id}"})
        except Exception as e:
            print(f"Error creating profile: {e}")
            
        return user

