from django.db import models

from apps.rbac.models import BaseModel


class MenuType(BaseModel):
    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_menu_name")
        ]

    def __str__(self):
        return f"- {self.name}"
