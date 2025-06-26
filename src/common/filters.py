from typing import Optional
from ninja import FilterSchema, Field
from django.db.models import Q
from django.utils import timezone


class UsersFilter(FilterSchema):
    """
    Filter schema for user endpoints.
    """

    favorite_toy: Optional[str] = Field(None, q="favorite_toy__icontains")
    username: Optional[str] = Field(None, q="username__icontains")
    search: Optional[str] = Field(
        None, q=["favorite_toy__icontains", "username__icontains"]
    )


class BarksFilter(FilterSchema):
    """
    Filter schema for bark endpoints.
    """

    message: Optional[str] = Field(None, q="message__icontains")
    trending: Optional[bool] = None

    def filter_trending(self, value: bool) -> Q:
        """Filter for trending barks"""
        if not value:
            return Q()
        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        return Q(created_at__gte=one_day_ago) & Q(sniff_count__gte=1)
