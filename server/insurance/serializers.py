from django.contrib.auth import get_user_model
from .models import Insurer, Agent, ServiceProvider, Surveyor, Policy
from rest_framework import serializers

User = get_user_model()

class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'
        
class PolicySerializer(serializers.ModelSerializer):
    insurer_id = serializers.PrimaryKeyRelatedField(
        queryset=Insurer.objects.all(), source='insurer', write_only=True
    )
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True
    )
    policy_holder_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='policy_holder', write_only=True, required=False
    )
    
    insurer = InsurerSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    
    class Meta:
        model = Policy
        fields = [
            'id', 'policy_number', 'policy_holder', 'policy_holder_id', 
            'insurer', 'insurer_id', 'agent', 'agent_id', 
            'policy_type', 'coverage_amount', 'premium_amount', 
            'start_date', 'end_date', 'status'
        ]

    def validate_coverage_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Coverage amount must be greater than zero.")
        return value

    def validate_premium_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Premium amount must be greater than zero.")
        return value

class SurveyorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surveyor
        fields = '__all__'
