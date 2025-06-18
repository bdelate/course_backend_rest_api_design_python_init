import base64
import json
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


class TimestampCursorPagination(PaginationBase):
    """
    Cursor pagination using timestamps.
    """

    class Input(Schema):
        cursor: Optional[str] = None
        limit: int = 10

    class Output(Schema):
        items: list[Any]
        next: Optional[str] = None
        next_cursor: Optional[str] = None

    def paginate_queryset(self, queryset, pagination: Input, **params):
        limit = min(pagination.limit, 100)
        cursor = pagination.cursor

        # Build the base URL from the current request
        request: HttpRequest = params.get("request")
        base_url = self._get_base_url(request)

        # Default ordering
        queryset = queryset.order_by("-created_at")

        # Decode cursor if provided
        filter_kwargs = {}
        if cursor:
            decoded = self.decode_cursor(cursor)
            if decoded is not None:
                # Use the timestamp from the cursor to filter results
                timestamp = decoded.get("timestamp")
                if timestamp:
                    filter_kwargs["created_at__lt"] = timestamp
            else:
                # If cursor is invalid, ignore it and return the latest items
                pass

        # Get one more than requested to determine if there's a next page
        results = list(queryset.filter(**filter_kwargs)[: limit + 1])

        # If we got more results than requested, there's a next page
        has_next = len(results) > limit
        if has_next:
            results = results[:-1]  # Remove the extra item

        # Generate the next cursor
        next_cursor = None
        if has_next and results:
            next_timestamp = results[-1].created_at.isoformat()
            next_cursor = self.encode_cursor({"timestamp": next_timestamp})

        return {
            "items": results,
            "next": f"{base_url}?cursor={next_cursor}&limit={limit}"
            if next_cursor
            else None,
            "next_cursor": next_cursor,
        }

    def decode_cursor(self, cursor):
        """Decode the cursor data from a URL-safe string"""
        if not cursor:
            return None
        try:
            decoded = base64.b64decode(cursor.encode()).decode()
            return json.loads(decoded)
        except (ValueError, json.JSONDecodeError):
            return None

    def encode_cursor(self, data):
        """Encode the cursor data into a URL-safe string"""
        json_str = json.dumps(data)
        encoded = base64.b64encode(json_str.encode()).decode()
        return encoded

    def _get_base_url(self, request):
        """Build the base URL without query parameters"""
        if not request:
            return ""

        # Get the full path without query parameters
        path = request.path

        # Get the scheme (http or https)
        scheme = "https" if request.is_secure() else "http"

        # Get the host
        host = request.get_host()

        # Construct the base URL
        return f"{scheme}://{host}{path}"
