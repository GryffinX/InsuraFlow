from rest_framework import viewsets
from .models import Insurer, Agent, Policy, ServiceProvider, Surveyor
from .serializers import InsurerSerializer, AgentSerializer, PolicySerializer, ServiceProviderSerializer, SurveyorSerializer
from accounts.permissions import IsAdmin, IsAgentOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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
    permission_classes = [IsAuthenticated, IsAgentOrAdmin]
    def get_queryset(self):
        user = self.request.user
        if user == "agent":
            return Policy.objects.filter(agent__email=user.email)
        if user == "admin":
            return Policy.objects.all()
        return Policy.objects.none()
    
    @action(detail=False, methods=["get"])
    def my_policies(self, req):
        user = req.user
        policies = Policy.objects.filter(policy_holder=user)
        serializer = self.get_serializer(policies, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def activate(self, request, pk=None):
        policy = self.get_object()
        policy.status = "active"
        policy.save()
        return Response({"message":"Policy activated"})
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def cancel(self, request, pk=None):
        policy = self.get_object()
        policy.status = "cancel"
        policy.save()
        return Response({"message":"Policy cancelled"})
    
    filterset_fields = ["status","policy_type"]
    search_fields = ["policy_field"]
    ordering_fields = ["start_date","coverage_amount"]

