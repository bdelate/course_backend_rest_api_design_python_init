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
from api.logic.auth_logic import handle_get_token, handle_refresh_token, handle_get_jwt_token, handle_refresh_jwt_token

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
    Endpoint to get a JWT access token using username and password.
    
    Args:
        request: The HTTP request
        credentials: The token request schema containing username and password
    
    Returns:
        A new JWT access token is returned if the credentials are valid,
        or an error if the credentials are invalid.
    """
    try:
        data = handle_get_jwt_token(
            username=credentials.username, password=credentials.password
        )
        return 200, data
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response

@router.post(
    "/jwt-token/refresh/",
    response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut},
    auth=None,
)
def refresh_jwt_token(request, refresh: RefreshTokenRequestSchemaIn):
    """
    Endpoint to refresh a JWT access token using a valid refresh token.
    
    Args:
        request: The HTTP request
        refresh: The refresh token schema containing the refresh token string
    
    Returns:
        A new JWT access token is returned if the refresh token is valid,
        or an error if the refresh token is invalid or expired.
    """
    try:
        data = handle_refresh_jwt_token(refresh.refresh_token)
        return 200, data
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response