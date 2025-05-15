from ninja import Router
from api.schemas.user_schemas import DogUserSchemaOut, DogUserCreateSchemaIn
from core.models import DogUserModel

router = Router()

@router.get("/", response=list[DogUserSchemaOut])
def users_list(request):
    """
    User list endpoint that returns a list of users.
    """
    return DogUserModel.objects.all()


@router.post("/", response={201: DogUserSchemaOut})
def create_user(request, user: DogUserCreateSchemaIn):
    """Create a new user."""
    data = user.dict()
    if DogUserModel.objects.filter(username=data['username']).exists():
        return 400, {"error": "Username already exists"}
    obj = DogUserModel.objects.create(**data)
    return 201, obj