import jwt
from django.conf import settings
import time
from ninja.security import HttpBearer
from core.models import DogUserModel

def create_jwt(user_id, token_type):
    """Create a JWT token for the user.

    Args:
        user_id (str): The ID of the user.
        token_type (str): The type of token (e.g., 'access', 'refresh').

    Returns:
        str: The encoded JWT token.
    """
    exp_seconds = 4 * 60 * 60 if token_type == 'access' else 7 * 24 * 60 * 60
    payload = {
        "user_id": str(user_id),
        "token_type": token_type,
        "iat": int(time.time()),
        "exp": int(time.time()) + exp_seconds,
      }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')



class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        """Authenticate a request using a JWT token.

        Args:
            request: The HTTP request
            token: The JWT token string from the Authorization header

        Returns:
            The user ID if authentication is successful, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
        try:
            assert payload['token_type'] == 'access'
            user = DogUserModel.objects.get(id=payload['user_id'])
            return user
        except (DogUserModel.DoesNotExist, AssertionError, KeyError):
            return None
            
