from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from .utils import send_otp_email
from .models import EmailOTP

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
        print(f"DEBUG: Registering with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send OTP
        send_otp_email(user)
        
        return Response({
            "user": UserSerializer(user).data,
            "message": "User registered successfully. Please verify your email with the OTP sent."
        }, status=status.HTTP_201_CREATED)

class VerifyOTPView(APIView):
    permission_classes = []

    def post(self, request):
        print(f"DEBUG: Verifying OTP with data: {request.data}")
        email = request.data.get('email')
        otp_code = request.data.get('otp')
        
        if not email or not otp_code:
            return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp_code, is_active=True).latest('created_at')
            
            # OTP is valid
            user.is_verified = True
            user.save()
            
            # Deactivate OTP
            otp_obj.is_active = False
            otp_obj.save()
            
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({"error": "Invalid OTP or Email"}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    permission_classes = []

    def post(self, request):
        print(f"DEBUG: Resending OTP with data: {request.data}")
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({"message": "Email is already verified"}, status=status.HTTP_400_BAD_REQUEST)
            
            send_otp_email(user)
            return Response({"message": "OTP resent successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .permissions import IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

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

class PasswordResetRequestView(APIView):
    permission_classes = []
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
            
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset email sent."})
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    permission_classes = []
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."})
            else:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

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
