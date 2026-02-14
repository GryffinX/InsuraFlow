from .models import Claim, InspectionReport, Settlement
from rest_framework import serializers
from insurance.serializers import PolicySerializer, ServiceProviderSerializer, SurveyorSerializer

class ClaimSerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    service_provider = ServiceProviderSerializer(read_only=True)
    class Meta:
        model = Claim
        fields = '__all__'

class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    claim = ClaimSerializer(read_only=True)
    surveyor = SurveyorSerializer(read_only=True)
    class Meta:
        model = Settlement
        fields = '__all__'