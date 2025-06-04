from core.models import DogUserModel


def handle_dog_users_list():
    """
    Handle the logic for listing dog users.
    Returns a list of all dog users.
    """
    return DogUserModel.objects.all()
