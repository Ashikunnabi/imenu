from django.db import models

from apps.core.rbac.models import BaseModel

from .attribute import Attribute
from .product import Product


class ProductAttribute(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="products")
    value = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "attribute"], name="unique_product_attribute"
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.attribute} - {self.value}"
