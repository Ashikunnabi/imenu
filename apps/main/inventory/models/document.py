from django.db import models

from apps.core.rbac.models import BaseModel


class Document(BaseModel):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    extension = models.CharField(max_length=256)
    is_encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
