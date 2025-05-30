from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.auth_schemas import TokenRequestSchemaOut, TokenRequestSchemaIn
from core.models import AuthTokenModel
from uuid import UUID
from django.contrib.auth import authenticate
router = Router()


@router.post("/token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_token(request, credentials: TokenRequestSchemaIn):
    """
    Endpoint to get an authentication token.
    
    Args:
        request: The HTTP request
        token_request: The token request schema containing username and password
    
    Returns:
        A token if authentication is successful, or an error if not.
    """
    user = authenticate(username=credentials.username, password=credentials.password)
    if user is None:
        return 401, {"error": "Invalid credentials"}
    token, _ = AuthTokenModel.objects.get_or_create(user=user)
    return 200, {"token": token.key}