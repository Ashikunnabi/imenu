from django.db import models

from apps.base.constants import ZERO
from apps.rbac.models import BaseModel


class Unit(BaseModel):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code", "name"], name="unique_unit_code_name")
        ]

    def __str__(self):
        return f"{self.code}-{self.name}"
