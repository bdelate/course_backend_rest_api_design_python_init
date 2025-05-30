from uuid import UUID
from ninja import Router
from api.schemas.user_schemas import DogUserSchemaOut, DogUserCreateSchemaIn, DogUserUpdateSchemaIn, DogUserWithTokenSchemaOut
from core.models import DogUserModel, AuthTokenModel
from api.schemas.common_schemas import ErrorSchemaOut

router = Router()

@router.get("/", response=list[DogUserSchemaOut])
def users_list(request):
    """
    User list endpoint that returns a list of users.
    """
    return DogUserModel.objects.all()


@router.get("/me/", response={200: DogUserSchemaOut})
def get_current_user(request):
    """
    Endpoint that returns the currently authenticated user.
    """
    return 200, request.auth


@router.post("/", response={201: DogUserWithTokenSchemaOut, 400: ErrorSchemaOut}, auth=None)
def create_user(request, user: DogUserCreateSchemaIn):
    """Create a new user."""
    data = user.dict()
    if DogUserModel.objects.filter(username=data['username']).exists():
        return 400, {"error": "Username already exists"}
    obj = DogUserModel.objects.create_user(**data)
    token = AuthTokenModel.objects.create(user=obj)
    return 201, {"user": obj, "token": token.key}

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