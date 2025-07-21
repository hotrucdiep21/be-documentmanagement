from apps.users.repositories import create_user_repo
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from core.exceptions import InvalidRefreshTokenException
from apps.users.repositories import update_user_repo


def login_user_service(serializer_data):
    return serializer_data


def register_user_service(validated_data):
    user = create_user_repo(
        email=validated_data['email'],
        password=validated_data['password'],
        full_name=validated_data['full_name']
    )
    return {
        "user_id": user.user_id,
        "email": user.email,
        "full_name": user.full_name
    }


def refresh_token_service(data):
    serializer = TokenRefreshSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
    except InvalidToken:
        raise InvalidRefreshTokenException()


def update_user_service(user, validated_data):
    updated_user = update_user_repo(user, validated_data)
    return {
        "user_id": updated_user.user_id,
        "email": updated_user.email,
        "full_name": updated_user.full_name
    }

def get_user_profile_service(user):
    return user
