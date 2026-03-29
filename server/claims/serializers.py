from .models import Claim, InspectionReport, Settlement
from rest_framework import serializers
from insurance.serializers import PolicySerializer, ServiceProviderSerializer, SurveyorSerializer

class ClaimSerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    service_provider = ServiceProviderSerializer(read_only=True)

    class Meta:
        model = Claim
        fields = '__all__'

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