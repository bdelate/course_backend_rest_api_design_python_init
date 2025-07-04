from ninja import ModelSchema, Schema, File
from core.models import DogUserModel
from pydantic import field_validator
from ninja.files import UploadedFile
from typing import Optional


class DogUserSchemaOut(ModelSchema):
    """Schema for dog user responses"""
    profile_image_url: Optional[str] = None

    class Meta:
        model = DogUserModel
        fields = ["id", "username", "favorite_toy"]

    @staticmethod
    def resolve_profile_image_url(obj):
        """Resolve the profile image URL"""
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return obj.profile_image.url
        return None


class DogUserCreateSchemaIn(ModelSchema):
    """Schema for dog user creation requests"""

    username: str

    class Meta:
        model = DogUserModel
        fields = ['username', 'password']

    @field_validator('username')
    @classmethod
    def validate_username_min_length(cls, v: str) -> str:
        """Ensure is at least 3 characters long"""
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v
    

class DogUserUpdateSchemaIn(ModelSchema):
    """Schema for updating dog users"""
    username: str | None = None
    favorite_toy: str | None = None

    class Meta:
        model = DogUserModel
        fields = ["username", "favorite_toy"]
        fields_optional = ["username", "favorite_toy"]


class DogUserWithTokenSchemaOut(Schema):
    """Schema for dog user with token response"""
    user: DogUserSchemaOut
    token: str

class ProfileImageUploadSchemaIn(Schema):
    """Schema for profile image upload"""
    image: UploadedFile = File(...)
