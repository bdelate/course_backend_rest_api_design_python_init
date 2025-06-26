import binascii
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from uuid import uuid4


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
    """Model representing a bark made by a dog."""

    user = models.ForeignKey(
        DogUserModel, on_delete=models.CASCADE, related_name="barks"
    )
    message = models.CharField(max_length=200)
    sniff_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Bark"
        verbose_name_plural = "Barks"

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}..."


class AuthTokenModel(BaseModel):
    """Represents an authentication token for a user"""

    TOKEN_TYPE_ACCESS = "access"
    TOKEN_TYPE_REFRESH = "refresh"
    TOKEN_TYPE_CHOICES = (
        (TOKEN_TYPE_ACCESS, "Access"),
        (TOKEN_TYPE_REFRESH, "Refresh"),
    )

    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(
        to=DogUserModel, related_name="auth_tokens", on_delete=models.CASCADE
    )
    token_type = models.CharField(
        max_length=10, choices=TOKEN_TYPE_CHOICES, default=TOKEN_TYPE_ACCESS
    )
    expires = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

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
            else:
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
        return f"{self.token_type.capitalize()} Token {self.key[:6]}... for {self.user.username}"


class UserSniffModel(BaseModel):
    """Represents a user's sniff (like) of a bark."""

    user = models.ForeignKey(
        DogUserModel, on_delete=models.CASCADE, related_name="sniffs"
    )
    bark = models.ForeignKey(
        BarkModel, on_delete=models.CASCADE, related_name="user_sniffs"
    )

    class Meta:
        verbose_name = "User Sniff"
        verbose_name_plural = "User Sniffs"
        # Ensure a user can only sniff a bark once
        unique_together = ("user", "bark")

    def __str__(self):
        return f"{self.user.username} sniffed {self.bark.message[:15]}..."
