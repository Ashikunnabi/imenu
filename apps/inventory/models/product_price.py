from django.contrib.auth import get_user_model
from django.db import models

from apps.base.constants import ZERO
from apps.rbac.models import BaseModel

from ..constants import ProductPriceTypes
from .product import Product

User = get_user_model()


class ProductPrice(BaseModel):
    type = models.CharField(
        choices=ProductPriceTypes.CHOICES, default=ProductPriceTypes.PURCHASE_PRICE, max_length=256
    )
    price = models.DecimalField(decimal_places=6, max_digits=18, default=ZERO)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")

    def __str__(self):
        return self.type
