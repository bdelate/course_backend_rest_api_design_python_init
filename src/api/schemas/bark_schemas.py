from ninja import Schema, ModelSchema
from core.models import BarkModel


class BarkSchemaOut(ModelSchema):
    """Schema for bark responses"""

    class Meta:
        model = BarkModel
        fields = ['id', 'message']



class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error: str

class BarkSchemaIn(Schema):
    """Schema for bark requests"""
    message: str
