import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Юзеры"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Наименование")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
