from rest_framework import viewsets
from .models import Claim, InspectionReport, Settlement
from .serializers import ClaimSerializer, InspectionReportSerializer, SettlementSerializer



# Create your views here.


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

class InspectionReportViewSet(viewsets.ModelViewSet):
    queryset = InspectionReport.objects.all()
    serializer_class = InspectionReportSerializer

class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
