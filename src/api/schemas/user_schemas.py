from ninja import ModelSchema
from core.models import DogUserModel
from pydantic import field_validator

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

    @field_validator('username')
    @classmethod
    def validate_username_min_length(cls, v: str) -> str:
        """Ensure is at least 3 characters long"""
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
