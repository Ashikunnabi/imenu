from django.db import models

from apps.base.validators import ScreenMethodValidator
from apps.rbac.models import BaseModel


class AttributeGroup(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"

    def screen_unique_name(self):
        if self.__class__.objects.filter(name=self.name).exclude(id=self.id).exists():
            return "Attribute with this name already exists."
