from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  
from .views import RegisterView, ProfileView, ChangePasswordView, CustomTokenObtainPairView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), 
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]