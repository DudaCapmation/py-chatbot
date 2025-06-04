from django.urls import path
from .views import register_user, logout_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"), # Returns access and refresh tokens
    path("logout/", logout_user, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]