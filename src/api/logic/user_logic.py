from common.filters import UsersFilter, apply_ordering
from core.models import DogUserModel, AuthTokenModel
from api.logic.exceptions import DuplicateResourceError, ResourceNotFoundError, InvalidFileError
from django.db.models import QuerySet
from ninja.files import UploadedFile
from django.core.files.storage import default_storage


def handle_dog_users_list(filters: UsersFilter) -> QuerySet[DogUserModel]:
    """
    Handle the logic for listing dog users.
    Returns a list of all dog users.
    """
    objs = DogUserModel.objects.all()
    queryset = filters.filter(objs)
    if filters.order_by:
        queryset = apply_ordering(
            queryset=queryset, order_by=filters.order_by, model_class=DogUserModel
        )
    return queryset



def handle_create_dog_user(username: str, password: str) -> tuple[DogUserModel, AuthTokenModel]:
    """
    Handle the logic for creating a new dog user.
    Returns the created user and their authentication token.
    """
    if DogUserModel.objects.filter(username=username).exists():
        raise DuplicateResourceError("Username already exists")
    
    user = DogUserModel.objects.create_user(username=username, password=password)
    token = AuthTokenModel.objects.create(user=user)
    
    return user, token

def handle_update_me(user: DogUserModel, data: dict) -> DogUserModel:
    """
    Handle the logic for updating the currently authenticated user.
    Returns the updated user object.
    """
    if 'username' in data and data['username'] != user.username:
        if DogUserModel.objects.filter(username=data['username']).exists():
            raise DuplicateResourceError("Username already exists")
    
    for attr, value in data.items():
        setattr(user, attr, value)
    
    user.save()
    return user

def handle_get_dog_user(user_id: int) -> DogUserModel:
    """
    Handle the logic for retrieving a dog user by ID.
    Returns the user object if found, otherwise raises an exception.
    """
    try:
        return DogUserModel.objects.get(id=user_id)
    except DogUserModel.DoesNotExist:
        raise ResourceNotFoundError("Dog user not found")
    

def handle_get_current_user(user: DogUserModel) -> DogUserModel:
    """
    Handle the logic for retrieving the currently authenticated user.
    Returns the user object.
    """
    return user


def handle_upload_profile_image(
    user: DogUserModel, image: UploadedFile
) -> DogUserModel:
    """
    Handle the logic for uploading a profile image.
    Validates the image and saves it to the user's profile.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if image.content_type not in allowed_types:
        raise InvalidFileError("Invalid image type")

    # Validate file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if image.size > max_size:
        raise InvalidFileError("Image size too large")

    # Delete old profile image if it exists
    if user.profile_image:
        if default_storage.exists(user.profile_image.name):
            default_storage.delete(user.profile_image.name)

    # Save new image
    user.profile_image = image
    user.save()
    return user