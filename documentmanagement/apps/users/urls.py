from django.urls import path
from apps.users.views import LoginAPIView
from apps.users.views import RegisterAPIView, RefreshTokenAPIView, UserUpdateAPIView, GetProfileAPIView, UploadAvatarAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='refresh_token'),
    path('me/', UserUpdateAPIView.as_view(), name='update_info'),
    path('profile/', GetProfileAPIView.as_view(), name='get_user_profile'),
    path('upload-avatar/', UploadAvatarAPIView.as_view(), name='upload-avatar'),
    # path('profile/' UserUpdateAPIView.as_view())
]
