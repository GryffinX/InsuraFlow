from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsAgentOrAdmin
from .models import Insurer, Agent, Policy, ServiceProvider, Surveyor
from .serializers import (
    InsurerSerializer, AgentSerializer, PolicySerializer, 
    ServiceProviderSerializer, SurveyorSerializer
)
from . import services

# Create your views here.

class InsurerViewSet(viewsets.ModelViewSet):
    queryset = Insurer.objects.all()
    serializer_class = InsurerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class SurveyorViewSet(viewsets.ModelViewSet):
    queryset = Surveyor.objects.all()
    serializer_class = SurveyorSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer
    
    def get_permissions(self):
        if self.action in ["activate", "cancel"]:
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ["list", "retrieve", "my_policies"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAgentOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "agent":
            return Policy.objects.filter(agent__email=user.email)
        if user.role == "admin":
            return Policy.objects.all()
        return Policy.objects.none()
    
    @action(detail=False, methods=["get"])
    def my_policies(self, request):
        user = request.user
        policies = Policy.objects.filter(policy_holder=user)
        serializer = self.get_serializer(policies, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        policy = self.get_object()
        services.activate_policy(policy)
        return Response({"message":"Policy activated"})
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        policy = self.get_object()
        services.cancel_policy(policy)
        return Response({"message":"Policy cancelled"})
    
    filterset_fields = ["status","policy_type"]
    search_fields = ["policy_number"]
    ordering_fields = ["start_date","coverage_amount"]

