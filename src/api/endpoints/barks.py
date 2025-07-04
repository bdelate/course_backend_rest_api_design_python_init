from ninja import Router, Query
from api.schemas.bark_schemas import (
    BarkSchemaOut,
    BarkCreateUpdateSchemaIn,
)
from api.schemas.common_schemas import ErrorSchemaOut
from uuid import UUID
from api.logic.bark_logic import (
    handle_create_bark,
    handle_barks_list,
    handle_get_bark,
    handle_delete_bark,
    handle_update_bark,
    handle_export_top_barks_csv,
)
from api.logic.exceptions import get_error_response
from ninja.pagination import paginate
from common.filters import BarksFilter


router = Router()


@router.get("/", response=list[BarkSchemaOut], auth=None)
@paginate
def barks_list(request, filters: BarksFilter = Query(...)):
    """
    Bark list endpoint that returns a list of barks.
    """
    objs = handle_barks_list(filters=filters)
    return objs


@router.get("/top-export/")
def export_top_barks_csv(request):
    """
    Endpoint for downloading a CSV of the user's top 10 most sniffed barks.
    """
    try:
        csv_response = handle_export_top_barks_csv(user=request.auth)
        return csv_response
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response

@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut}, auth=None)
def get_bark(request, bark_id: UUID):
    """
    Bark detail endpoint that returns a single bark.
    """
    try:
        bark_instance = handle_get_bark(bark_id)
        return 200, bark_instance
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response


@router.delete("/{bark_id}/", response={204: None, 404: ErrorSchemaOut})
def delete_bark(request, bark_id: UUID):
    """Delete a bark."""
    try:
        handle_delete_bark(bark_id, request.auth)
        return 204, None
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response


@router.put("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def update_bark(request, bark_id: UUID, bark: BarkCreateUpdateSchemaIn):
    """Update an existing bark."""
    try:
        updated_bark = handle_update_bark(bark_id, request.auth, bark.dict())
        return 200, updated_bark
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response


@router.post("/", response={201: BarkSchemaOut})
def create_bark(request, bark: BarkCreateUpdateSchemaIn):
    """Create a new bark."""
    new_bark = handle_create_bark(user=request.auth, data=bark.dict())
    return 201, new_bark
