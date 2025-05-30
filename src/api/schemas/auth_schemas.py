from ninja import Schema


class TokenRequestSchemaIn(Schema):
    """Schema for token request with username and password"""

    username: str
    password: str


class TokenRequestSchemaOut(Schema):
    """Schema for token response"""

    access_token: str
    refresh_token: str
    expires_in: int


class RefreshTokenRequestSchemaIn(Schema):
    """Schema for refresh token request"""
    refresh_token: str
