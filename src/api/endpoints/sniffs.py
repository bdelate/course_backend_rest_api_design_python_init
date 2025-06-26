from ninja import Router
from api.schemas.sniff_schemas import SniffSchemaOut, SniffCreateSchemaIn
from api.logic.sniff_logic import handle_create_sniff
from api.logic.exceptions import get_error_response
from api.schemas.common_schemas import ErrorSchemaOut

router = Router()


@router.post(
    "/", response={201: SniffSchemaOut, 409: ErrorSchemaOut, 404: ErrorSchemaOut}
)
def create_sniff(request, sniff: SniffCreateSchemaIn):
    """Sniff to a bark"""
    try:
        bark = handle_create_sniff(bark_id=sniff.bark_id, user=request.auth)
        return 201, bark
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response
