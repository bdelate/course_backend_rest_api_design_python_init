from ninja import Router
from api.schemas.user_schemas import DogUserSchemaOut
from core.models import DogUserModel

router = Router()

@router.get("/", response=list[DogUserSchemaOut])
def users_list(request):
    """
    User list endpoint that returns a list of users.
    """
    return DogUserModel.objects.all()