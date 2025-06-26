from typing import Optional
from ninja import FilterSchema, Field

class UsersFilter(FilterSchema):
    """Filter schema for user endpoints."""

    favorite_toy: Optional[str] = Field(None, q="favorite_toy__icontains")
    username: Optional[str] = Field(None, q="username__icontains")


class BarksFilter(FilterSchema):
    """Filter schema for bark endpoints."""

    message: Optional[str] = Field(None, q="message__icontains")