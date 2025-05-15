from ninja import Router
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.bark_schemas import BarkSchemaOut, BarkCreateUpdateSchemaIn
from core.models import BarkModel, DogUserModel
from uuid import UUID

router = Router()


@router.get("/", response=list[BarkSchemaOut])
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.s
    """
    return BarkModel.objects.all()


@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def get_bark(request, bark_id: UUID):
    """
    Bark detail endpoint that returns a single bark.
    """
    bark = BarkModel.objects.filter(id=bark_id).first()
    if bark:
        return 200, bark
    return 404, {"error": "Bark not found"}


@router.delete("/{bark_id}/", response={204: None, 404: ErrorSchemaOut})
def delete_bark(request, bark_id: UUID):
    """Delete a bark."""
    bark_instance = BarkModel.objects.filter(id=bark_id).first()
    if not bark_instance:
        return 404, {"error": "Bark not found"}

    # Delete the bark instance
    bark_instance.delete()
    return 204, None


@router.put("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def update_bark(request, bark_id: UUID, bark: BarkCreateUpdateSchemaIn):
    """Update an existing bark."""
    bark_instance = BarkModel.objects.filter(id=bark_id).first()
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
    data = bark.dict()
    data['user_id'] = DogUserModel.objects.first().id
    obj = BarkModel.objects.create(**data)
    return 201, obj
