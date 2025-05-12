from ninja import Schema, ModelSchema
from core.models import BarkModel
from api.schemas.user_schemas import DogUserSchemaOut

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
        """Resolve created date in format 2023-10-01 from created_at field"""
        return obj.created_at.strftime("%Y-%m-%d")




class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error: str

class BarkSchemaIn(Schema):
    """Schema for bark requests"""
    message: str
