from .models import Claim, InspectionReport, Settlement
from rest_framework import serializers
from insurance.models import Policy, ServiceProvider, Surveyor
from insurance.serializers import PolicySerializer, ServiceProviderSerializer, SurveyorSerializer

class ClaimSerializer(serializers.ModelSerializer):
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.all(), source='policy', write_only=True
    )
    service_provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all(), source='service_provider', write_only=True
    )
    
    policy = PolicySerializer(read_only=True)
    service_provider = ServiceProviderSerializer(read_only=True)

    class Meta:
        model = Claim
        fields = [
            'id', 'policy', 'policy_id', 'service_provider', 'service_provider_id',
            'claim_date', 'claim_amount', 'claim_reason', 'status'
        ]

    def validate_claim_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Claim amount must be greater than zero.")
        return value

class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    claim_id = serializers.PrimaryKeyRelatedField(
        queryset=Claim.objects.all(), source='claim', write_only=True
    )
    claim = ClaimSerializer(read_only=True)

    class Meta:
        model = Settlement
        fields = [
            'id', 'claim', 'claim_id', 'approved_amount', 
            'settlement_date', 'payment_mode', 'payment_status'
        ]

    def validate(self, data):
        claim = data.get('claim')
        approved_amount = data.get('approved_amount')

        if claim and approved_amount and approved_amount > claim.claim_amount:
             raise serializers.ValidationError({
                 "approved_amount": f"Approved amount ({approved_amount}) cannot exceed the claim amount ({claim.claim_amount})."
             })
        return data
