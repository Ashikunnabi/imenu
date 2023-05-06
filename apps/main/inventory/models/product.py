from django.contrib.auth import get_user_model
from django.db import models

from apps.core.rbac.models import BaseModel

from .brand import Brand
from .group import Group
from .type import Type
from .unit import Unit
from .vat import Vat

User = get_user_model()


class Product(BaseModel):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default="")
    short_description = models.CharField(max_length=256, blank=True, default="")
    family = models.CharField(max_length=256, blank=True, default="")
    series = models.CharField(max_length=256, blank=True, default="")

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="products")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code"], name="unique_product_code"
            )
        ]

    def __str__(self):
        return f"{self.code}-{self.name}"
