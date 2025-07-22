from apps.users.models import User
from django.contrib.auth import authenticate


def get_user_by_email_and_password(email, password):
     return authenticate(email=email, password=password)

def create_user_repo(email, password, full_name) -> User:
    return User.objects.create_user(
        email=email,
        password=password,
        full_name=full_name
    )


def update_user_repo(user, data) -> User:
    for attr, value in data.items():
        setattr(user, attr, value)
    user.save()
    return user


def update_user_avatar_repo(user, avatar_url)->User:
    user.avatar = avatar_url
    user.save()
    return user

