from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsAdmin, IsAgentOrAdmin, IsProvider, IsCustomer
from .models import Provider, Agent, Policy, ServiceProvider, Surveyor, UserPolicy
from .serializers import (
    ProviderSerializer, AgentSerializer, PolicySerializer, 
    ServiceProviderSerializer, SurveyorSerializer,
    UserPolicySerializer
)
from datetime import date, timedelta
import random

class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'provider__company_name']
    filterset_fields = ['policy_type', 'is_active']
    ordering_fields = ['premium_amount', 'coverage_amount']
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Policy.objects.filter(is_active=True)
        
        if user.role == 'admin':
            return Policy.objects.all()
        if user.role == 'provider':
            return Policy.objects.filter(provider__user=user)
        if user.role == 'agent':
            return Policy.objects.all() # Agents can see all to recommend
        
        return Policy.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsProvider() | IsAdmin() | IsAgentOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'provider':
            serializer.save(provider=user.provider_profile)
        elif user.role == 'agent':
            if user.agent_profile.provider:
                serializer.save(provider=user.agent_profile.provider)
            else:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"detail": "Agent is not assigned to any provider."})
        elif user.role == 'admin':
            serializer.save()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only providers, agents, or admins can create policies.")

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsProvider | IsAdmin])
    def customers(self, request, pk=None):
        policy = self.get_object()
        customers = UserPolicy.objects.filter(policy=policy)
        return Response(UserPolicySerializer(customers, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def buy(self, request, pk=None):
        policy = self.get_object()
        
        user_id = request.data.get('user_id')
        if user_id and request.user.role in ['agent', 'admin']:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            agent = request.user.agent_profile if request.user.role == 'agent' else None
        else:
            if request.user.role != 'customer':
                return Response({"error": "Only customers can buy directly, or agents/admins must specify user_id."}, status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            agent = None
        
        if UserPolicy.objects.filter(user=user, policy=policy, status='active').exists():
            return Response({"error": "User already owns an active instance of this policy"}, status=status.HTTP_400_BAD_REQUEST)
        
        policy_number = f"UP-{random.randint(100000, 999999)}"
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        
        user_policy = UserPolicy.objects.create(
            user=user,
            policy=policy,
            policy_number=policy_number,
            start_date=start_date,
            end_date=end_date,
            status='active',
            agent=agent
        )
        
        return Response(UserPolicySerializer(user_policy, context={'request': request}).data, status=status.HTTP_201_CREATED)

class UserPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserPolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return UserPolicy.objects.all()
        if user.role == 'agent':
            return UserPolicy.objects.filter(agent__user=user)
        if user.role == 'customer':
            return UserPolicy.objects.filter(user=user)
        if user.role == 'provider':
            return UserPolicy.objects.filter(policy__provider__user=user)
        return UserPolicy.objects.none()

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsProvider]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Agent.objects.all()
        if user.role == 'provider':
            return Agent.objects.filter(provider__user=user)
        return Agent.objects.none()

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]

class SurveyorViewSet(viewsets.ModelViewSet):
    queryset = Surveyor.objects.all()
    serializer_class = SurveyorSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin | IsProvider]
