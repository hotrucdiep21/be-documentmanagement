from rest_framework.exceptions import APIException
from rest_framework import status
class InvalidRefreshTokenException(APIException):
    status_code=status.HTTP_401_UNAUTHORIZED
    default_detail="Invalid token refresh"
    default_code='invalid_refresh_token'