from ninja import Router
from api.schemas.bark_schemas import BarkSchemaOut

router = Router()


@router.get("/", response=list[BarkSchemaOut])
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    return [{'id':1, 'message': 'bark 1!'}, {'id':2, 'message': 'bark 2!'}, {'id':3, 'message': 'bark 3!'}]


@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: dict})
def get_bark(request, bark_id: int):
    """
    Bark detail endpoint that returns a single bark.
    """
    if bark_id in [1, 2, 3]:
        return 200, {"id": bark_id, "message": f"bark {bark_id}!", "breed": "Poodle"}
    return 404, {"error": "Bark not found"}


@router.delete("/{bark_id}/", response={204: None, 404: dict})
def delete_bark(request, bark_id: int):
    if bark_id in [1, 2, 3]:
        return 204, None
    return 404, {"error": "Bark not found"}
