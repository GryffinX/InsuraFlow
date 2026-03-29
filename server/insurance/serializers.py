from .models import Insurer, Agent, ServiceProvider, Surveyor, Policy
from rest_framework import serializers

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
    insurer = InsurerSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    
    class Meta:
        model = Policy
        fields = '__all__'

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

