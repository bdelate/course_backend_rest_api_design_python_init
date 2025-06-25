from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.bark_schemas import BarkSchemaOut, BarkCreateUpdateSchemaIn
from uuid import UUID
from api.logic.bark_logic import handle_create_bark, handle_barks_list, handle_get_bark, handle_delete_bark, handle_update_bark
from api.logic.exceptions import get_error_response
from ninja.pagination import paginate

router = Router()


@router.get("/", response=list[BarkSchemaOut], auth=None)
@paginate
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    objs = handle_barks_list()
    return objs


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
