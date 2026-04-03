from .models import Claim, InspectionReport, Settlement
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from insurance.models import UserPolicy, ServiceProvider, Surveyor
from insurance.serializers import UserPolicySerializer, ServiceProviderSerializer, SurveyorSerializer

class ClaimSerializer(serializers.ModelSerializer):
    policy = serializers.CharField(source='user_policy.policy.title', read_only=True)
    amount = serializers.DecimalField(source='claim_amount', max_digits=12, decimal_places=2, read_only=True)
    created_at = serializers.DateField(source='claim_date', read_only=True)
    
    user_policy_id = serializers.PrimaryKeyRelatedField(
        queryset=UserPolicy.objects.all(), source='user_policy', write_only=True
    )
    service_provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all(), source='service_provider', write_only=True, required=False
    )
    
    user_policy = UserPolicySerializer(read_only=True)
    service_provider = ServiceProviderSerializer(read_only=True)
    assigned_surveyor = SurveyorSerializer(read_only=True)
    assigned_surveyor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='surveyor'), source='assigned_surveyor', write_only=True, required=False
    )

    class Meta:
        model = Claim
        fields = [
            'id', 'policy', 'amount', 'created_at', 'status',
            'user_policy', 'user_policy_id', 'service_provider', 'service_provider_id',
            'assigned_surveyor', 'assigned_surveyor_id',
            'claim_date', 'claim_amount', 'claim_reason', 'documents'
        ]

    def validate(self, attrs):
        user_policy = attrs.get('user_policy')
        if user_policy and user_policy.status != 'active':
            raise serializers.ValidationError({"user_policy": "You can only file a claim for an active policy."})
        
        # Check if user owns the policy (if not agent/admin)
        request = self.context.get('request')
        if request and request.user.role == 'customer' and user_policy.user != request.user:
            raise serializers.ValidationError({"user_policy": "You do not own this policy."})
            
        return attrs

    def validate_claim_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Claim amount must be greater than zero.")
        return value

class InspectionReportSerializer(serializers.ModelSerializer):
    surveyor = SurveyorSerializer(read_only=True)
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
        # Handle both create (with claim_id mapped to claim) and update
        claim = data.get('claim')
        approved_amount = data.get('approved_amount')

        if claim and approved_amount and approved_amount > claim.claim_amount:
             raise serializers.ValidationError({
                 "approved_amount": f"Approved amount ({approved_amount}) cannot exceed the claim amount ({claim.claim_amount})."
             })
        return data
