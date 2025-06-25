from typing import Optional
from core.models import DogUserModel, AuthTokenModel
from api.logic.exceptions import DuplicateResourceError, ResourceNotFoundError
from django.db.models import QuerySet

def handle_dog_users_list(favorite_toy: Optional[str] = None) -> QuerySet[DogUserModel]:
    """
    Handle the logic for listing dog users.
    Returns a list of all dog users.
    """
    objs = DogUserModel.objects.all()
    if favorite_toy:
        objs = objs.filter(favorite_toy=favorite_toy)
    return objs


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