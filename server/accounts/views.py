from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import RegisterSerializer, UserSerializer

# Create your views here.

User = get_user_model()

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "user": UserSerializer(user).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)

from rest_framework import viewsets
from .permissions import IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email', 'phone']
    filterset_fields = ['role', 'is_verified']
    pagination_class = None

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def verify(self, request, pk=None):
        user = self.get_object()
        user.is_verified = True
        user.save()
        return Response({"message": "User verified successfully."})

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def reject(self, request, pk=None):
        user = self.get_object()
        # You can choose to delete or deactivate
        user.is_active = False
        user.save()
        return Response({"message": "User rejected and deactivated."})

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        else:
            user.set_password('Insuraflow@123')
            user.save()
            
        # Auto-create corresponding profiles
        from insurance.models import Provider, Agent, Surveyor
        try:
            if user.role == 'provider':
                Provider.objects.get_or_create(user=user, defaults={'company_name': user.username, 'contact_email': user.email})
            elif user.role == 'agent':
                Agent.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email})
            elif user.role == 'surveyor':
                Surveyor.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email, 'license_no': f"LNC-{user.id}", 'region': 'Unassigned'})
        except Exception as e:
            print(f"Error creating profile: {e}")

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        password = self.request.data.get('password')
        if password:
            instance = serializer.save()
            instance.set_password(password)
            instance.save()
        else:
            serializer.save()
