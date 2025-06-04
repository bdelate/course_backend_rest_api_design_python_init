from api.logic.exceptions import AuthenticationError, TokenExpiredError, TokenInvalidError
from common.auth.jwt_auth import create_jwt
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

def handle_refresh_token(refresh_token: str) -> dict:
    """
    Handle the logic for refreshing an authentication token.

    Args:
        refresh_token: The refresh token string

    Returns:
        A dictionary containing a new access and refresh token, or raises TokenInvalidError or TokenExpiredError if the token is invalid or expired.
    """
    try:
        refresh = AuthTokenModel.objects.get(key=refresh_token, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    except AuthTokenModel.DoesNotExist:
        raise TokenInvalidError("Invalid refresh token")

    if not refresh.is_valid():
        raise TokenExpiredError("Expired refresh token")

    # Delete existing tokens for the user
    AuthTokenModel.objects.filter(user=refresh.user).delete()

    # Create new access and refresh tokens
    access_token = AuthTokenModel.objects.create(user=refresh.user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    new_refresh_token = AuthTokenModel.objects.create(user=refresh.user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)

    return {
        "access_token": access_token.key,
        "refresh_token": new_refresh_token.key,
        "expires_in": int((access_token.expires - timezone.now()).total_seconds())
    }

def handle_get_jwt_token(username: str, password: str) -> dict:
    """
    Handle the logic for getting a JWT token.

    Args:
        username: The username of the user
        password: The password of the user

    Returns:
        A dictionary containing a JWT token, or raises an AuthenticationError if authentication fails.
    """
    user = authenticate(username=username, password=password)
    if user is None:
        raise AuthenticationError("Invalid credentials")

    
    access_token = create_jwt(user.id, 'access')
    refresh_token = create_jwt(user.id, 'refresh')
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 14400  # 4 hours in seconds
    }