from core.models import DogUserModel, BarkModel
from api.logic.exceptions import ResourceNotFoundError
from common.filters import BarksFilter, apply_ordering
from django.db.models import QuerySet
import csv
from io import StringIO
from django.http import HttpResponse


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



def handle_barks_list(filters: BarksFilter) -> QuerySet[BarkModel]:
    """
    Handle the logic for retrieving a list of barks.
    Returns a list of BarkModel instances.
    """
    objs = BarkModel.objects.select_related("user").all()
    queryset = filters.filter(objs)
    if filters.trending:
        queryset = queryset.order_by("-sniff_count")
    elif filters.order_by:
        queryset = apply_ordering(
            queryset=queryset, order_by=filters.order_by, model_class=BarkModel
        )
    return queryset



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


def handle_export_top_barks_csv(user: DogUserModel) -> HttpResponse:
    """
    Handle the logic for exporting user's top 10 sniffed barks as CSV.
    Returns an HttpResponse with CSV content.
    """
    # Get the user's top 10 most sniffed barks
    top_barks = (
        BarkModel.objects.select_related("user")
        .filter(user=user, sniff_count__gt=0)
        .order_by("-sniff_count")[:10]
    )

    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)

    # Write CSV header
    writer.writerow(["Message", "Sniff Count", "Created At", "Username"])

    # Write bark data
    for bark in top_barks:
        writer.writerow(
            [
                bark.message,
                bark.sniff_count,
                bark.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                bark.user.username,
            ]
        )

    # Create HTTP response with CSV content
    response = HttpResponse(output.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="top_barks.csv"'

    return response