from django.db import models

from apps.rbac.models import BaseModel


class Warehouse(BaseModel):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    location = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code", "name"], name="unique_warehouse_code_name")
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
