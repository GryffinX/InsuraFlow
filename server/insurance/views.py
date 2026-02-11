from rest_framework import viewsets
from .models import Insurer, Agent, Policy, ServiceProvider, Surveyor
from .serializers import InsurerSerializer, AgentSerializer, PolicySerializer, ServiceProviderSerializer, SurveyorSerializer

# Create your views here.

class InsurerViewSet(viewsets.ModelViewSet):
    queryset = Insurer.objects.all()
    serializer_class = InsurerSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class SurveyorViewSet(viewsets.ModelViewSet):
    queryset = Surveyor.objects.all()
    serializer_class = SurveyorSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
