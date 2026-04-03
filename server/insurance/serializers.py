from django.contrib.auth import get_user_model
from .models import Provider, Agent, ServiceProvider, Surveyor, Policy, UserPolicy
from rest_framework import serializers

User = get_user_model()

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(), source='provider', write_only=True, required=False
    )
    class Meta:
        model = Agent
        fields = '__all__'

class SurveyorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(), source='provider', write_only=True, required=False, allow_null=True
    )
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            'id', 'title', 'description', 'policy_type', 
            'coverage_amount', 'premium_amount', 
            'provider', 'provider_id', 'is_active', 'is_owned'
        ]

    def get_is_owned(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserPolicy.objects.filter(user=request.user, policy=obj).exists()
        return False

class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserPolicySerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.all(), source='policy', write_only=True
    )
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True, required=False, allow_null=True
    )
    user = UserSerializerSimple(read_only=True)
    
    class Meta:
        model = UserPolicy
        fields = '__all__'
