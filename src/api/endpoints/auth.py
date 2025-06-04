from django.conf import settings
import jwt
from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.auth_schemas import TokenRequestSchemaOut, TokenRequestSchemaIn, RefreshTokenRequestSchemaIn
from core.models import AuthTokenModel, DogUserModel
from django.contrib.auth import authenticate
from django.utils import timezone
from common.auth.jwt_auth import create_jwt
from api.logic.exceptions import get_error_response
from api.logic.auth_logic import handle_get_token, handle_refresh_token

router = Router()


@router.post("/token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_token(request, credentials: TokenRequestSchemaIn):
    """
    Endpoint to get an authentication token.
    
    Args:
        request: The HTTP request
        credentials: The token request schema containing username and password
    
    Returns:
        A new access and refresh token is returned if the credentials are valid,
        or an error if the credentials are invalid.
    """
    try:
        response = handle_get_token(credentials.username, credentials.password)
        return 200, response
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response

@router.post("/token/refresh/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def refresh_token(request, refresh_token: RefreshTokenRequestSchemaIn):
    """
    Endpoint to refresh an authentication token using a valid refresh token.
    
    Args:
        request: The HTTP request
        refresh_token: The refresh token schema containing the refresh token string
    
    Returns:
        A new access and refresh token is returned if the refresh token is valid,
        or an error if the refresh token is invalid or expired.
    """
    try:
        response = handle_refresh_token(refresh_token.refresh_token)
        return 200, response
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response

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

@router.post(
    "/jwt-token/refresh/",
    response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut},
    auth=None,
)
def refresh_jwt_token(request, refresh: RefreshTokenRequestSchemaIn):
    """
    Endpoint to refresh a JWT access token using a valid refresh token.
    """
    try:
        payload = jwt.decode(
            refresh.refresh_token, settings.JWT_SECRET, algorithms=["HS256"]
        )
    except jwt.DecodeError:
        return 401, {"error": "Invalid refresh token"}
    except jwt.ExpiredSignatureError:
        return 401, {"error": "Expired refresh token"}

    try:
        user_id = payload["user_id"]
        assert payload["token_type"] == "refresh"
        user = DogUserModel.objects.get(id=user_id)
    except (KeyError, AssertionError, DogUserModel.DoesNotExist):
        return 401, {"error": "Invalid refresh token"}

    access_token = create_jwt(user_id=user.id, token_type="access")
    refresh_token = create_jwt(user_id=user.id, token_type="refresh")

    return 200, {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 14400,  # 4 hours in seconds
    }