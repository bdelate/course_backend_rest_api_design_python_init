from uuid import UUID
from ninja import Router
from api.logic.exceptions import get_error_response
from api.schemas.user_schemas import DogUserSchemaOut, DogUserCreateSchemaIn, DogUserUpdateSchemaIn, DogUserWithTokenSchemaOut
from core.models import DogUserModel
from api.schemas.common_schemas import ErrorSchemaOut
from api.logic.user_logic import handle_dog_users_list, handle_create_dog_user

router = Router()



@router.get("/", response=list[DogUserSchemaOut])
def dog_users_list(request):
    """
    Endpoint that returns a list of dog users.
    """
    users = handle_dog_users_list()
    return 200, users



@router.get("/me/", response={200: DogUserSchemaOut})
def get_current_user(request):
    """
    Endpoint that returns the currently authenticated user.
    """
    return 200, request.auth


@router.post("/", response={201: DogUserWithTokenSchemaOut, 409: ErrorSchemaOut}, auth=None)
def create_user(request, user: DogUserCreateSchemaIn):
    """Create a new user."""
    try:
        user_obj, token_obj = handle_create_dog_user(username=user.username, password=user.password)
    except Exception as e:
        status_code, error_response = get_error_response(e)
        return status_code, error_response
    return 201, {"user": user_obj, "token": token_obj.key}

@router.get("/{user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def get_user(request, user_id: UUID):
    """Get a user by ID."""
    try:
        obj = DogUserModel.objects.get(id=user_id)
    except DogUserModel.DoesNotExist:
        return 404, {"error": "Dog user not found"}
    return obj

@router.patch("/me/", response={200: DogUserSchemaOut, 400: ErrorSchemaOut})
def update_me(request, user: DogUserUpdateSchemaIn):
    """Update a user by ID."""
    obj = request.auth
    data = user.dict(exclude_unset=True)
    if 'username' in data and data['username'] != obj.username:
        if DogUserModel.objects.filter(username=data['username']).exists():
            return 400, {"error": "Username already exists"}
    for attr, value in data.items():
        setattr(obj, attr, value)
    obj.save()
    return 200, obj