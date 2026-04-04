from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # standard validation first
        data = super().validate(attrs)
        
        # self.user is set by super().validate() if successful
        if not self.user:
            raise serializers.ValidationError("Invalid credentials")
            
        return data

class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

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
        read_only_fields = ['is_verified']

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
            "secret_key",
        ]

    def validate(self, attrs):
        role = attrs.get('role', 'customer')
        secret_key = attrs.get('secret_key')
        
        from django.conf import settings
        if role != 'customer':
            expected_key = {
                'admin': settings.ADMIN_SECRET_KEY,
                'agent': settings.AGENT_SECRET_KEY,
                'provider': settings.PROVIDER_SECRET_KEY,
                'surveyor': settings.SURVEYOR_SECRET_KEY,
            }.get(role)
            
            if not secret_key or secret_key != expected_key:
                raise serializers.ValidationError({"secret_key": "Invalid or missing secret key for this role."})
        
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
                Surveyor.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email, 'license_no': f"LNC-{user.id}", 'region': 'Unassigned'})
        except Exception as e:
            # Profile creation should not block user registration
            pass
            
        return user
