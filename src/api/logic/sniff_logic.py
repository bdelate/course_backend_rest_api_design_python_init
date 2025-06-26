from core.models import BarkModel, UserSniffModel
from api.logic.exceptions import ResourceNotFoundError, DuplicateResourceError


def handle_create_sniff(bark_id: str, user) -> BarkModel:
    """Handle creating a sniff (like) on a bark"""
    try:
        bark = BarkModel.objects.get(id=bark_id)
    except BarkModel.DoesNotExist:
        raise ResourceNotFoundError("Bark not found")

    # Check if the user has already sniffed this bark
    if UserSniffModel.objects.filter(user=user, bark=bark).exists():
        raise DuplicateResourceError("You've already sniffed this bark")

    # Create the sniff
    UserSniffModel.objects.create(user=user, bark=bark)

    # Increment the sniff count
    bark.sniff_count += 1
    bark.save()
    return bark
