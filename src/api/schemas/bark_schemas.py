from ninja import Schema, ModelSchema
from core.models import BarkModel
from api.schemas.user_schemas import DogUserSchemaOut

class BarkSchemaOut(ModelSchema):
    """Schema for bark responses"""

    user: DogUserSchemaOut

    class Meta:
        model = BarkModel
        fields = ['id', 'message']




class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error: str

class BarkSchemaIn(Schema):
    """Schema for bark requests"""
    message: str
