from ninja.security import HttpBearer
from core.models import AuthTokenModel

class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        """Authenticate a request using a token.

        Args:
            request: The HTTP request
            token: The token string from the Authorization header

        Returns:
            The user if authentication successful, None otherwise
        """
        try:
            auth_token = AuthTokenModel.objects.select_related('user').get(key=token)
            if auth_token.is_valid():
                return auth_token.user
        except AuthTokenModel.DoesNotExist:
            return None
        return None