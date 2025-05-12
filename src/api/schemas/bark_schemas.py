from ninja import Schema, ModelSchema
from core.models import BarkModel
from api.schemas.user_schemas import DogUserSchemaOut
from pydantic import field_validator

class BarkSchemaOut(ModelSchema):
    """Schema for bark responses"""

    user: DogUserSchemaOut
    created_time: str
    created_date: str

    class Meta:
        model = BarkModel
        fields = ["id", "message"]

    @staticmethod
    def resolve_created_time(obj):
        """Resolve created time in format 06:12pm from created_at field"""
        return obj.created_at.strftime("%I:%M %p")
    
    @staticmethod
    def resolve_created_date(obj):
        """Resolve the created date in format 15Jan25 from the created_at field"""
        return obj.created_at.strftime("%d%b%y")


class BarkCreateUpdateSchemaIn(ModelSchema):
    """Schema for bark creation requests"""

    message: str

    class Meta:
        model = BarkModel
        fields = ["message"]

    @field_validator('message')
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        """Ensure message isn't just whitespace"""
        if not v.strip():
            raise ValueError("Message cannot be empty or just whitespace")
        return v

class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error: str
