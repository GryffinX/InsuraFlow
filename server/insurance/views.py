from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsAdmin, IsAgentOrAdmin, IsProvider, IsCustomer, IsVerifiedUser
from .models import Provider, Agent, Policy, ServiceProvider, Surveyor, UserPolicy
from .serializers import (
    ProviderSerializer, AgentSerializer, PolicySerializer, 
    ServiceProviderSerializer, SurveyorSerializer,
    UserPolicySerializer
)
from datetime import date, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'provider__company_name', 'provider__user__username']
    filterset_fields = {
        'policy_type': ['exact'],
        'is_active': ['exact'],
        'premium_amount': ['gte', 'lte'],
        'coverage_amount': ['gte', 'lte'],
        'provider': ['exact'],
    }
    ordering_fields = ['premium_amount', 'coverage_amount']

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            # Safely log body if possible
            try:
                logger.info(f"Policy API Request: {request.method} {request.path} Body: {request.body.decode('utf-8')}")
            except:
                logger.info(f"Policy API Request: {request.method} {request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Policy.objects.filter(is_active=True)
        
        if user.role == 'provider':
            # Providers only see their own policies
            return Policy.objects.filter(provider__user=user)
        
        # Admin, Agent, and others see all active policies
        # Admin can see inactive ones too if needed, let's allow all for admin
        if user.role == 'admin':
            return Policy.objects.all()
            
        return Policy.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        # All CRUD operations require authentication and verification
        perms = [IsAuthenticated(), IsVerifiedUser()]
        
        if self.action == 'create':
            perms.append(IsProvider() | IsAgent() | IsAdmin())
        elif self.action in ['update', 'partial_update', 'destroy']:
            perms.append(IsProvider() | IsAdmin())
            
        return perms

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role == 'provider':
            provider = getattr(user, 'provider_profile', None)
            if not provider:
                raise ValidationError("Provider profile not found.")
            serializer.save(provider=provider)
        elif user.role == 'agent':
            agent = getattr(user, 'agent_profile', None)
            if not agent or not agent.provider:
                raise ValidationError("Agent is not properly assigned to a provider.")
            serializer.save(provider=agent.provider)
        elif user.role == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("Only providers, agents, or admins can create policies.")

    def update(self, request, *args, **kwargs):
        logger.info(f"Policy API Update - Method: {request.method}, Data: {request.data}")
        try:
            partial = kwargs.pop('partial', False)
            if request.method == 'PATCH':
                partial = True
            
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Policy update failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()
        if user.role == 'provider' and instance.provider.user != user:
            raise PermissionDenied("You can only edit your own policies.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == 'provider' and instance.provider.user != user:
            raise PermissionDenied("You can only delete your own policies.")
        instance.delete()

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsProvider | IsAdmin])
    def customers(self, request, pk=None):
        policy = self.get_object()
        # Ensure provider only sees customers for their own policy
        if request.user.role == 'provider' and policy.provider.user != request.user:
            raise PermissionDenied("You do not have access to this policy's customer list.")
        customers = UserPolicy.objects.filter(policy=policy)
        return Response(UserPolicySerializer(customers, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsVerifiedUser])
    def buy(self, request, pk=None):
        policy = self.get_object()
        
        user_id = request.data.get('user_id')
        if user_id and request.user.role in ['agent', 'admin']:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            agent = getattr(request.user, 'agent_profile', None) if request.user.role == 'agent' else None
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

    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated()]

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
    permission_classes = [IsAuthenticated, IsAdmin, IsVerifiedUser]

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsProvider, IsVerifiedUser]

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
        return [IsAuthenticated(), IsAdmin(), IsVerifiedUser()]

class SurveyorViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyorSerializer
    
    def get_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(role="surveyor")
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin | IsProvider, IsVerifiedUser()]
