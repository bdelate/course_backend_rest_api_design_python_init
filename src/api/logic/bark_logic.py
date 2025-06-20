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
    return BarkModel.objects.all()


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


def handle_delete_bark(bark_id: str, user: DogUserModel) -> None:
    """
    Handle the logic for deleting a bark.
    
    Args:
        bark_id: The ID of the bark to delete.
        user: The user who is attempting to delete the bark.
    
    Raises:
        ResourceNotFoundError: If the bark with the given ID does not exist or does not belong to the user.
    """
    bark = BarkModel.objects.filter(id=bark_id, user=user).first()
    if not bark:
        raise ResourceNotFoundError("Bark not found")
    
    # Delete the bark instance
    bark.delete()


def handle_update_bark(bark_id: str, user: DogUserModel, data: dict) -> BarkModel:
    """
    Handle the logic for updating an existing bark.
    
    Args:
        bark_id: The ID of the bark to update.
        user: The user who is updating the bark.
        data: The new data for the bark.
    
    Returns:
        BarkModel: The updated bark object.
    
    Raises:
        ResourceNotFoundError: If the bark with the given ID does not exist or does not belong to the user.
    """
    bark = BarkModel.objects.filter(id=bark_id, user=user).first()
    if not bark:
        raise ResourceNotFoundError("Bark not found")
    
    # Update the bark instance with the new data
    for attr, value in data.items():
        setattr(bark, attr, value)
    bark.save()
    
    return bark