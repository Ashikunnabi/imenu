from django.db import models

from apps.rbac.models import BaseModel


class Document(BaseModel):
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to ='uploads/% Y/% m/% d/', max_length=500, null=True)
    extension = models.CharField(max_length=256)
    is_encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
