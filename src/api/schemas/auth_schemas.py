from ninja import Schema


class TokenRequestSchemaIn(Schema):
    """
    Schema for token request input.
    """
    username: str
    password: str

class TokenRequestSchemaOut(Schema):
    """
    Schema for token request output.
    """
    token: str