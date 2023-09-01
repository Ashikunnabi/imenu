from django.db import models
from apps.base.constants import ZERO

from apps.rbac.models import BaseModel
from apps.inventory.models.unit import Unit

from .product import Product


class ProductUnit(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="units")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="products")
    max = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)
    min = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)

    def __str__(self):
        return f"{self.product} - {self.unit.name}"
