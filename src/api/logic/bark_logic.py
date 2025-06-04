from core.models import BarkModel, DogUserModel

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