from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.auth_schemas import TokenRequestSchemaOut, TokenRequestSchemaIn, RefreshTokenRequestSchemaIn
from core.models import AuthTokenModel
from django.contrib.auth import authenticate
from django.utils import timezone
from common.auth.jwt_auth import create_jwt

router = Router()


@router.post("/token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_token(request, credentials: TokenRequestSchemaIn):
    """
    Endpoint to get an authentication token.
    
    Args:
        request: The HTTP request
        token_request: The token request schema containing username and password
    
    Returns:
        A access and refresh token if authentication is successful,
    """
    user = authenticate(username=credentials.username, password=credentials.password)
    if user is None:
        return 401, {"error": "Invalid credentials"}
    AuthTokenModel.objects.filter(user=user).delete()
    access = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access.expires - timezone.now()).total_seconds())
    return 200, {
        "access_token": access.key,
        "refresh_token": refresh.key,
        "expires_in": expires_in
    }

@router.post("/token/refresh/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def refresh_token(request, refresh_token: RefreshTokenRequestSchemaIn):
    """
    Endpoint to refresh an authentication token.
    
    Args:
        request: The HTTP request
        refresh_token: The refresh token string
    
    Returns:
        A new access and refresh is returned if the refresh token is valid,
        or an error if the refresh token is invalid.
    """
    try:
        refresh = AuthTokenModel.objects.get(key=refresh_token.refresh_token, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    except AuthTokenModel.DoesNotExist:
        return 401, {"error": "Invalid refresh token"}
    if not refresh.is_valid():
        return 401, {"error": "Expired refresh token"}
    
    AuthTokenModel.objects.filter(user=refresh.user).delete()
    user = refresh.user
    AuthTokenModel.objects.filter(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS).delete()
    access = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access.expires - timezone.now()).total_seconds())
    return 200, {
        "access_token": access.key,
        "refresh_token": refresh.key,
        "expires_in": expires_in
    }

@router.post(
    "/jwt-token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None
)
def get_jwt_token(request, credentials: TokenRequestSchemaIn):
    """
    Endpoint to get a JWT token.
    
    Args:
        request: The HTTP request
        credentials: The token request schema containing username and password
    
    Returns:
        A JWT access and refresh token if authentication is successful,
        or an error if the credentials are invalid.
    """
    user = authenticate(username=credentials.username, password=credentials.password)
    if user is None:
        return 401, {"error": "Invalid credentials"}
    
    access_token = create_jwt(user.id, 'access')
    refresh_token = create_jwt(user.id, 'refresh')
    
    return 200, {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 14400  # 4 hours in seconds
    }
