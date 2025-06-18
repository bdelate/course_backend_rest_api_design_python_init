from typing import Any
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

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        return {
            'items': queryset[skip : skip + per_page],
            'total': queryset.count(),
            'pages': (queryset.count() + per_page - 1) // per_page,
            'per_page': per_page,
            'skip': skip,
        }
