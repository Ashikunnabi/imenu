from django.db import models

from apps.base.validators import ScreenMethodValidator
from apps.rbac.models import BaseModel

from .attribute_group import AttributeGroup


class Attribute(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)
    attribute_group = models.ForeignKey(
        AttributeGroup, on_delete=models.CASCADE, related_name="attributes"
    )

    def __str__(self):
        return f"{self.name}"

    def screen_unique_name(self):
        if (
            self.__class__.objects.filter(
                name=self.name,
                attribute_group=self.attribute_group,
            )
            .exclude(id=self.id)
            .exists()
        ):
            return "Attribute with this name already exists."
