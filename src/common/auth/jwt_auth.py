import jwt
from django.conf import settings
import time

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