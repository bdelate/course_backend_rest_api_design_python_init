class LogicError(Exception):
    """Base exception for all API logic errors"""
    pass


class DuplicateResourceError(LogicError):
    """Raised when attempting to create a resource that already exists"""
    pass


class ResourceNotFoundError(LogicError):
    """Raised when a requested resource is not found"""
    pass

class AuthenticationError(LogicError):
    """Raised when authentication fails"""
    pass

class TokenInvalidError(LogicError):
    """Raised when a token is invalid or expired"""
    pass

class TokenExpiredError(LogicError):
    """Raised when a token has expired"""
    pass

class InvalidFileError(LogicError):
    """Raised when an invalid file is uploaded"""

    pass


EXCEPTION_TO_HTTP_STATUS = {
    DuplicateResourceError: 409,
    ResourceNotFoundError: 404,
    AuthenticationError: 401,
    TokenInvalidError: 401,
    TokenExpiredError: 401,
    InvalidFileError: 400,
    LogicError: 500,
}


def get_error_response(exception: Exception) -> tuple[int, dict]:
    """
    Convert an exception to an appropriate HTTP status code and error response.

    Args:
        exception: The exception that was raised

    Returns:
        tuple: (status_code, error_response_dict)
    """
    # Find most specific exception type in the mapping
    for exception_type, status_code in EXCEPTION_TO_HTTP_STATUS.items():
        if isinstance(exception, exception_type):
            return status_code, {"error": str(exception)}

    # Default fallback for unexpected exceptions
    return 500, {"error": "An unexpected error occurred"}
