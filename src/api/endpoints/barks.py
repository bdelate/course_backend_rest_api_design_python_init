from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.bark_schemas import BarkSchemaOut, BarkCreateUpdateSchemaIn
from core.models import BarkModel
from uuid import UUID
from api.logic.bark_logic import handle_create_bark, handle_barks_list, handle_get_bark, handle_delete_bark
from api.logic.exceptions import get_error_response

router = Router()


@router.get("/", response=list[BarkSchemaOut], auth=None)
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.s
    """
    barks = handle_barks_list()
    return 200, barks


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
    bark_instance = BarkModel.objects.filter(id=bark_id, user=request.auth).first()
    if not bark_instance:
        return 404, {"error": "Bark not found"}

    # Update the bark instance with the new data
    for attr, value in bark.dict().items():
        setattr(bark_instance, attr, value)
    bark_instance.save()
    return 200, bark_instance


@router.post("/", response={201: BarkSchemaOut})
def create_bark(request, bark: BarkCreateUpdateSchemaIn):
    """Create a new bark."""
    new_bark = handle_create_bark(user=request.auth, data=bark.dict())
    return 201, new_bark
