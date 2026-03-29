from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsCustomer, IsSurveyor, IsAdmin
from .models import Claim, InspectionReport, Settlement
from .serializers import ClaimSerializer, InspectionReportSerializer, SettlementSerializer
from . import services

# Create your views here.

class ClaimViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimSerializer

    def get_permissions(self):
        if self.action in ["approve", "reject", "settle"]:
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ["list", "retrieve", "my_claims"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Claim.objects.all()
        if user.role == "customer":
            return Claim.objects.filter(policy__policy_holder=user)
        if user.role == "agent":
            return Claim.objects.filter(policy__agent__email=user.email)
        if user.role == "surveyor":
            return Claim.objects.all()
        return Claim.objects.none()

    @action(detail=False, methods=["get"])
    def my_claims(self, request):
        user = request.user
        claims = Claim.objects.filter(policy__policy_holder=user)
        serializer = self.get_serializer(claims, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        claim = self.get_object()
        services.submit_claim(claim)
        return Response({"message": "Claim submitted for review"})

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        claim = self.get_object()
        services.approve_claim(claim)
        return Response({"message": "Claim approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        claim = self.get_object()
        services.reject_claim(claim)
        return Response({"message": "Claim rejected"})

    @action(detail=True, methods=["post"])
    def settle(self, request, pk=None):
        claim = self.get_object()
        services.settle_claim(claim)
        return Response({"message": "Claim settled"})

    
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
