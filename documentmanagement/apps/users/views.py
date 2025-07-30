from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import LoginSerializer, RegisterSerializer, UserUpdateSerializer, UserProfileSerializer, UploadAvatarSerializer
from apps.users.services import login_user_service, register_user_service, refresh_token_service, update_user_service, get_user_profile_service,upload_avatar_service
from core.mixins import ResponseMixi


class LoginAPIView(APIView, ResponseMixi):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login_user_service(serializer.validated_data)
        return Response(self.format_response(result, "Login successfully", status.HTTP_200_OK))


class RegisterAPIView(APIView, ResponseMixi):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = register_user_service(serializer.validated_data)
        return Response(self.format_response(result, "Register a account succeffully", status.HTTP_201_CREATED))


class RefreshTokenAPIView(APIView, ResponseMixi):
    permission_classes = [AllowAny]

    def post(self, request):
        result = refresh_token_service(request.data)
        return Response(self.format_response(result, "Refresh token successfully", status.HTTP_200_OK))


class UserUpdateAPIView(APIView, ResponseMixi):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        print("request.user", request.user)
        serializer = UserUpdateSerializer(
            data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = update_user_service(user, serializer.validated_data)
        return Response(self.format_response(
            result, "Update user info successfully", status.HTTP_200_OK
        ))


class GetProfileAPIView(APIView, ResponseMixi):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_profile_service(request.user)
        serializer = UserProfileSerializer(user)
        return Response(self.format_response(serializer.data, "Get profile successfully"))


class UploadAvatarAPIView(APIView, ResponseMixi):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UploadAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result=upload_avatar_service(user, serializer.validated_data)
        return Response(self.format_response(result, "Avatar uploaded successfully"))
    

