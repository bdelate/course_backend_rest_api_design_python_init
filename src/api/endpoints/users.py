from uuid import UUID
from ninja import Router
from api.schemas.user_schemas import DogUserSchemaOut, DogUserCreateSchemaIn, DogUserUpdateSchemaIn
from core.models import DogUserModel
from api.schemas.common_schemas import ErrorSchemaOut

router = Router()

@router.get("/", response=list[DogUserSchemaOut])
def users_list(request):
    """
    User list endpoint that returns a list of users.
    """
    return DogUserModel.objects.all()


@router.post("/", response={201: DogUserSchemaOut, 400: ErrorSchemaOut})
def create_user(request, user: DogUserCreateSchemaIn):
    """Create a new user."""
    data = user.dict()
    if DogUserModel.objects.filter(username=data['username']).exists():
        return 400, {"error": "Username already exists"}
    obj = DogUserModel.objects.create(**data)
    return 201, obj

@router.get("/{user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def get_user(request, user_id: UUID):
    """Get a user by ID."""
    try:
        obj = DogUserModel.objects.get(id=user_id)
    except DogUserModel.DoesNotExist:
        return 404, {"error": "Dog user not found"}
    return obj

@router.patch("/{user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def update_user(request, user_id: UUID, user: DogUserUpdateSchemaIn):
    """Update a user by ID."""
    try:
        obj = DogUserModel.objects.get(id=user_id)
    except DogUserModel.DoesNotExist:
        return 404, {"error": "Dog user not found"}
    
    data = user.dict(exclude_unset=True)
    for attr, value in data.items():
        setattr(obj, attr, value)
    obj.save()
    return obj