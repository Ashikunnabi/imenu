from django.db import models
from django.contrib.auth import get_user_model

from apps.rbac.models import BaseModel
from apps.inventory.models import Brand, Product
from apps.table.models.table import Table

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="carts", null=True)
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="carts", null=True)
    total_price_in_vat = models.DecimalField(max_digits=18, decimal_places=8)
    total_price_ex_vat = models.DecimalField(max_digits=18, decimal_places=8)

    @property
    def vat(self):
        vat = self.total_price_in_vat - self.total_price_ex_vat
        return vat
