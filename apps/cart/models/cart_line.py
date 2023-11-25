from django.contrib.auth import get_user_model
from django.db import models

from apps.inventory.models import Product
from apps.rbac.models import BaseModel

from .cart import Cart

User = get_user_model()


class CartLine(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name="lines")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="cart_lines"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_in_vat = models.DecimalField(max_digits=18, decimal_places=8)
    price_ex_vat = models.DecimalField(max_digits=18, decimal_places=8)
    total_price_in_vat = models.DecimalField(max_digits=18, decimal_places=8)
    total_price_ex_vat = models.DecimalField(max_digits=18, decimal_places=8)
    extra_info = models.JSONField(blank=True, null=True)

    @property
    def vat(self):
        vat = self.total_price_in_vat - self.total_price_ex_vat
        return vat
