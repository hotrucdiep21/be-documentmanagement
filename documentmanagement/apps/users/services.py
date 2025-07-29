from apps.users.repositories import create_user_repo
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import InvalidRefreshTokenException
from apps.users.serializers import UserProfileSerializer
from apps.users.repositories import update_user_repo, update_user_avatar_repo, get_user_by_email_and_password
from core.supabase import upload_to_supabase


def login_user_service(data):
    user = get_user_by_email_and_password(data['email'], data['password'])
    if not user:
        raise ValueError("Invalid email or password")
    if not user.is_active:
        raise ValueError("User is inactive")
    refresh = RefreshToken.for_user(user)
    profile_data = UserProfileSerializer(user).data

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': profile_data
    }


def register_user_service(data):
    user = create_user_repo(**data)
    return UserProfileSerializer(user).data


def refresh_token_service(data):
    return data


def update_user_service(user, data):
    avatar_file = data.pop("avatar", None)
    if avatar_file:
        avatar_url = upload_to_supabase(avatar_file, folder="avatars")
        data["avatar"] = avatar_url
    updated_user = update_user_repo(user, data)
    return UserProfileSerializer(updated_user).data


def get_user_profile_service(user):
    return user


def upload_avatar_service(user, data):
    avatar_file = data['avatar']
    avatar_url = upload_to_supabase(avatar_file, folder='avatars')
    updated_user = update_user_avatar_repo(user, avatar_url)
    return UserProfileSerializer(updated_user).data
