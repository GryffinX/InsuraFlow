from rest_framework import viewsets
from .models import Claim, InspectionReport, Settlement
from .serializers import ClaimSerializer, InspectionReportSerializer, SettlementSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer, IsSurveyor, IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class ClaimViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    def get_queryset(self):
        user = self.request.user
        return Claim.objects.filter(policy__policy_holder=user)
    
    @action(detail=False, methods=["get"])
    def my_claims(self, req):
        user = req.user
        claims = Claim.objects.filter(policy__policy_holder=user)
        serializer = self.get_serializer(claims, many=True)
        return Response(serializer.data)



    @action(detail=True, methods=["post"])
    def submit(self, response, pk=None):
        claim = self.get_object()
        
        if claim.status != "filed":
            return Response({"error":"Only new claims can be submitted"},
                            status=status.HTTP_400_BAD_REQUEST)
        claim.status="under_review"
        claim.save()

        return Response({"message":"Claim submitted for review"})
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def approve(self, response, pk=None):
        claim = self.get_object()

        if claim.status != "under_review":
            return Response({"error": "Claim must be under review"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        claim.status="approved"
        claim.save()

        return Response({"message":"Claim approved"})
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def reject(self, response, pk=None):
        claim = self.get_object()

        if claim.status != "under_review":
            return Response({"error":"Claim must be under review"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        claim.status="rejected"
        claim.save()

        return Response({"message":"Claim rejected"})
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def settle(self, response, pk=None):
        claim = self.get_object()

        if claim.status != "approved":
            return Response({"error":"Claim must be approved"},
                            status=status.HTTP_400_BAD_REQUEST)

        claim.status="settled"
        claim.save()

        return Response({"message":"Claim settled"})
    
    filterset_fields = ["status"]
    search_fields = ["claim_reason"]
    ordering_fields = ["claim_date","claim_amount"]

class InspectionReportViewSet(viewsets.ModelViewSet):
    serializer_class = InspectionReportSerializer
    permission_classes = [IsAuthenticated, IsSurveyor]
    def get_queryset(self):
        user = self.request.user
        return InspectionReport.objects.filter(surveyor__email=user.email)
    filterset_fields = ["damage_level"]
    ordering_fields = ["inspection_date"]


class SettlementViewSet(viewsets.ModelViewSet):
    serializer_class = SettlementSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    def get_queryset(self):
        return Settlement.objects.all() 
    filterset_fields = ["payment_status","payment_mode"]
    ordering_fields = ["settlement_date"]
