from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer  
    permission_classes = [AllowAny]  

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer 
    permission_classes = [IsAuthenticated] 
    
    def get_object(self):
        return self.request.user.userprofile

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer