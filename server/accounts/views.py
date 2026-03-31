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

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
