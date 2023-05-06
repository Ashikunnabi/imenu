from django.db import models

from apps.core.rbac.models import BaseModel


class Type(BaseModel):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code", "name"], name="unique_type_code_name")
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
