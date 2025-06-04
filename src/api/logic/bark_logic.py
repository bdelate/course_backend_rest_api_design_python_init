from core.models import BarkModel, DogUserModel
from api.logic.exceptions import ResourceNotFoundError

def handle_create_bark(user: DogUserModel, data: dict) -> BarkModel:
    """
    Handle the logic for creating a new bark.
    
    Args:
        user: The user who is creating the bark.
        data: The data for the new bark, including text and possibly media.
    
    Returns:
        BarkModel: The created bark object.
    """
    data["user_id"] = user.id
    bark = BarkModel.objects.create(user=user, **data)
    return bark


def handle_barks_list() -> list[BarkModel]:
    """
    Handle the logic for retrieving a list of barks.
    
    Returns:
        list[BarkModel]: A list of all barks.
    """
    return list(BarkModel.objects.all())


def handle_get_bark(bark_id: str) -> BarkModel:
    """
    Handle the logic for retrieving a single bark by its ID.
    
    Args:
        bark_id: The ID of the bark to retrieve.
    
    Returns:
        BarkModel: The requested bark object.
    
    Raises:
        ResourceNotFoundError: If the bark with the given ID does not exist.
    """
    bark = BarkModel.objects.filter(id=bark_id).first()
    if not bark:
        raise ResourceNotFoundError("Bark not found")
    return bark