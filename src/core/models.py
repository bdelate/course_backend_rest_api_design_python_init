from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import binascii
import os
from django.utils import timezone


class BaseModel(models.Model):
    """Contains common fields intended to be inherited by all models"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    

class AuthTokenModel(BaseModel):
    """Represents an authentication token for a user"""

    TOKEN_TYPE_ACCESS = "access"
    TOKEN_TYPE_REFRESH = "refresh"
    TOKEN_TYPE_CHOICES = [
        (TOKEN_TYPE_ACCESS, "Access Token"),
        (TOKEN_TYPE_REFRESH, "Refresh Token"),
    ]

    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(
        to=DogUserModel, related_name="auth_tokens", on_delete=models.CASCADE
    )
    expires = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    token_type = models.CharField(
        max_length=10, choices=TOKEN_TYPE_CHOICES, default=TOKEN_TYPE_ACCESS
    )

    class Meta:
        verbose_name = "Auth Token"
        verbose_name_plural = "Auth Tokens"
        unique_together = ("user", "token_type")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        if self.expires is None:
            if self.token_type == self.TOKEN_TYPE_ACCESS:
                self.expires = timezone.now() + timezone.timedelta(hours=4)
            elif self.token_type == self.TOKEN_TYPE_REFRESH:
                self.expires = timezone.now() + timezone.timedelta(days=7)
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def is_expired(self):
        if self.expires is None:
            return False
        return timezone.now() >= self.expires

    def is_valid(self):
        return self.is_active and not self.is_expired()

    def __str__(self):
        return f"Token {self.key[:6]}... for {self.user.username}"
