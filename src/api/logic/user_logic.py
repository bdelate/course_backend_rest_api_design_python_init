from core.models import DogUserModel, AuthTokenModel


def handle_dog_users_list():
    """
    Handle the logic for listing dog users.
    Returns a list of all dog users.
    """
    return DogUserModel.objects.all()


def handle_create_dog_user(username: str, password: str) -> tuple[DogUserModel, AuthTokenModel]:
    """
    Handle the logic for creating a new dog user.
    Returns the created user and their authentication token.
    """
    if DogUserModel.objects.filter(username=username).exists():
        raise ValueError("Username already exists")
    
    user = DogUserModel.objects.create_user(username=username, password=password)
    token = AuthTokenModel.objects.create(user=user)
    
    return user, token