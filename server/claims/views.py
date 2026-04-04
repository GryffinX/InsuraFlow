from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsCustomer, IsSurveyor, IsAdmin, IsProvider, IsAgent, IsVerifiedUser
from .models import Claim, InspectionReport, Settlement
from .serializers import ClaimSerializer, InspectionReportSerializer, SettlementSerializer

# Create your views here.

class ClaimViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'assign_surveyor', 'approve', 'reject']:
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Claim.objects.all()
        if user.role == "customer":
            return Claim.objects.filter(user=user)
        if user.role == "provider":
            return Claim.objects.filter(user_policy__policy__provider__user=user)
        if user.role == "agent":
            return Claim.objects.filter(user_policy__agent__user=user)
        if user.role == "surveyor":
            return Claim.objects.filter(assigned_surveyor=user)
        return Claim.objects.none()

    def perform_create(self, serializer):
        user_policy = serializer.validated_data.get('user_policy')
        request_user = self.request.user
        
        # If agent or admin, allow filing on behalf of the customer
        if request_user.role in ['agent', 'admin']:
            user = user_policy.user
        else:
            if user_policy.user != request_user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only file a claim for a policy you own.")
            user = request_user
            
        serializer.save(user=user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdmin | IsProvider | IsAgent])
    def assign_surveyor(self, request, pk=None):
        claim = self.get_object()
        surveyor_id = request.data.get('surveyor_id')
        if not surveyor_id:
            return Response({"error": "surveyor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        claim.assigned_surveyor_id = surveyor_id
        claim.status = 'under_review'
        claim.save()
        return Response({"message": "Surveyor assigned successfully"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        claim = self.get_object()
        if request.user.role == 'surveyor' and claim.assigned_surveyor != request.user:
            return Response({"error": "Not assigned to this claim"}, status=status.HTTP_403_FORBIDDEN)
        if request.user.role not in ['admin', 'surveyor']:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        claim.status = 'approved'
        claim.save()
        return Response({"message": "Claim approved"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        claim = self.get_object()
        if request.user.role == 'surveyor' and claim.assigned_surveyor != request.user:
            return Response({"error": "Not assigned to this claim"}, status=status.HTTP_403_FORBIDDEN)
        if request.user.role not in ['admin', 'surveyor']:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        claim.status = 'rejected'
        claim.save()
        return Response({"message": "Claim rejected"})

class InspectionReportViewSet(viewsets.ModelViewSet):
    serializer_class = InspectionReportSerializer
    permission_classes = [IsAuthenticated, IsSurveyor | IsAdmin, IsVerifiedUser]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return InspectionReport.objects.all()
        return InspectionReport.objects.filter(surveyor=user)

    def perform_create(self, serializer):
        serializer.save(surveyor=self.request.user)

class SettlementViewSet(viewsets.ModelViewSet):
    serializer_class = SettlementSerializer
    permission_classes = [IsAuthenticated, IsAdmin, IsVerifiedUser]

    def get_queryset(self):
        return Settlement.objects.all()

    def perform_create(self, serializer):
        settlement = serializer.save()
        claim = settlement.claim
        claim.status = 'settled'
        claim.save()
