from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import LoginSerializer, RegisterSerializer
from apps.users.services import login_user_service, register_user_service, refresh_token_service
from core.mixins import ResponseMixi

class LoginAPIView(APIView, ResponseMixi):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result=login_user_service(serializer.validated_data)
        return Response(self.format_response(result, "Login successfully", status.HTTP_200_OK))
    
class RegisterAPIView(APIView, ResponseMixi):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = register_user_service(serializer.validated_data)
        return Response(self.format_response(result, "Register a account succeffully", status.HTTP_201_CREATED))
    
class RefreshTokenAPIView(APIView, ResponseMixi):
    permission_classes=[AllowAny]
    
    def post(self, request):
        result=refresh_token_service(request.data)
        return Response(self.format_response(result, "Refresh token successfully", status.HTTP_200_OK))