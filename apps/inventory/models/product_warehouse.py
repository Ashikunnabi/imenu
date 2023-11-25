from django.db import models
from apps.base.constants import ZERO

from apps.rbac.models import BaseModel

from .product import Product
from .warehouse import Warehouse


class ProductWarehouse(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="warehouses")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="products")
    stock = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)

    def __str__(self):
        return f"{self.product} - {self.warehouse} - {self.stock}"
