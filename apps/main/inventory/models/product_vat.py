from django.db import models
from apps.core.base.constants import ZERO

from apps.core.rbac.models import BaseModel
from apps.main.inventory.models.vat import Vat

from .product import Product


class ProductVat(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="vats")
    vat = models.ForeignKey(Vat, on_delete=models.CASCADE, related_name="products")
    flat = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)
    percentage = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)

    def __str__(self):
        return f"{self.product} - {self.vat.name}- {self.flat} - {self.percentage}"
