from django.contrib.auth import get_user_model
from django.db import models

from apps.rbac.models import BaseModel

from ..constants import ProductCodeTypes
from .product import Product

User = get_user_model()


class ProductCode(BaseModel):
    type = models.CharField(
        choices=ProductCodeTypes.CHOICES, default=ProductCodeTypes.UPC, max_length=256
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="codes")
    value = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "type"], name="unique_product_type"
            )
        ]

    def __str__(self):
        return self.type
