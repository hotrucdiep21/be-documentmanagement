from django.urls import path
from apps.users.views import LoginAPIView
from apps.users.views import RegisterAPIView, RefreshTokenAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='refresh_token')
]