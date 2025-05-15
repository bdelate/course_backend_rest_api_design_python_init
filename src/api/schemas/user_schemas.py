from ninja import ModelSchema
from core.models import DogUserModel

class DogUserSchemaOut(ModelSchema):
    """Schema for dog user responses"""

    class Meta:
        model = DogUserModel
        fields = ['id', 'username']


class DogUserCreateSchemaIn(ModelSchema):
    """Schema for dog user creation requests"""

    class Meta:
        model = DogUserModel
        fields = ['username']
