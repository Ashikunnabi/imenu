from django.db import models
from apps.base.validators import ScreenMethodValidator

from apps.rbac.models import BaseModel


class TableType(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_table_name")
        ]

    def __str__(self):
        return f"- {self.name}"

    def screen_unique_name(self):
        if self.__class__.objects.filter(name=self.name).exclude(id=self.id).exists():
            return "Table type with this name already exists."
