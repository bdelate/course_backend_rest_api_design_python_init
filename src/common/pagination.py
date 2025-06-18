from typing import Any, Optional
from django.http import HttpRequest
from ninja.pagination import PaginationBase
from ninja import Schema


class SkipPagination(PaginationBase):
    """
    Custom pagination class that allows skipping a number of items
    and specifying the number of items per page.
    """
    class Input(Schema):
        skip: int = 0
        per_page: int = 5


    class Output(Schema):
        items: list[Any]
        total: int
        pages: int
        per_page: int
        skip: int
        next: Optional[str] = None
        previous: Optional[str] = None

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        count = queryset.count()

        # Build the base URL from the current request
        request: HttpRequest = params.get("request")
        base_url = self._get_base_url(request)

        # Calculate next and previous links
        next_link = None
        previous_link = None

        # If there are more items after this page
        if skip + per_page < count:
            next_link = f"{base_url}?skip={skip + per_page}&per_page={per_page}"

        # If we're not on the first page
        if skip > 0:
            # Calculate the previous skip value (don't go below 0)
            prev_skip = max(0, skip - per_page)
            previous_link = f"{base_url}?skip={prev_skip}&per_page={per_page}"

        return {
            "items": queryset[skip : skip + per_page],
            "total": queryset.count(),
            "pages": (queryset.count() + per_page - 1) // per_page,
            "per_page": per_page,
            "skip": skip,
            "next": next_link,
            "previous": previous_link,
        }

    def _get_base_url(self, request):
        """Build the base URL without query parameters"""
        if not request:
            return ''

        # Get the full path without query parameters
        path = request.path

        # Get the scheme (http or https)
        scheme = 'https' if request.is_secure() else 'http'

        # Get the host
        host = request.get_host()

        # Construct the base URL
        return f"{scheme}://{host}{path}"
