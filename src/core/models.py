from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """Contains common fields intended to be inherited by all models"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class DogUserModel(AbstractUser, BaseModel):
    """Custom user model for dog users."""

    favorite_toy = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Dog User"
        verbose_name_plural = "Dog Users"

    def __str__(self):
        return self.username


class BarkModel(BaseModel):
    """Model representing a bark."""

    message = models.CharField(max_length=200)
    user = models.ForeignKey(DogUserModel, on_delete=models.CASCADE, related_name="barks")

    class Meta:
        verbose_name = "Bark"
        verbose_name_plural = "Barks"

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}..."