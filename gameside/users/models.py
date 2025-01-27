from django.conf import settings
from django.db import models

# Create your models here.


class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token'
    )
    key = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
