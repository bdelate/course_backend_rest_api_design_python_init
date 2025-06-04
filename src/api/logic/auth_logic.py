from api.logic.exceptions import AuthenticationError
from core.models import DogUserModel, AuthTokenModel
from django.contrib.auth import authenticate
from django.utils import timezone


def handle_get_token(username: str, password: str) -> dict:
    """
    Handle the logic for getting an authentication token.

    Args:
        username: The username of the user
        password: The password of the user

    Returns:
        A dictionary containing access and refresh tokens, or raises an AuthenticationError if authentication fails.
    """
    user = authenticate(username=username, password=password)
    if user is None:
        raise AuthenticationError("Invalid credentials")

    AuthTokenModel.objects.filter(user=user).delete()
    access_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)

    return {
        "access_token": access_token.key,
        "refresh_token": refresh_token.key,
        "expires_in": int((access_token.expires - timezone.now()).total_seconds())
    }