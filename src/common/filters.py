from typing import Optional
from ninja import Schema

class UsersFilter(Schema):
    """
    Filter schema for user endpoints.
    """
    favorite_toy: Optional[str] = None
    username: Optional[str] = None
