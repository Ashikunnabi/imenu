from django.db import models
from django.contrib.auth import get_user_model

from apps.rbac.models import BaseModel
from apps.table.models.table import Table

User = get_user_model()


class Order(BaseModel):
    placed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="orders", null=True)
    total_price_in_vat = models.DecimalField(decimal_places=8, max_digits=18)
    total_price_ex_vat = models.DecimalField(decimal_places=8, max_digits=18)
    extra_info = models.JSONField(blank=True, null=True)
    # def __str__(self):
    #     return self.user.name

    def created_date(self):
        return self.created_at.strftime("%B %d, %Y")

    @property
    def vat(self):
        vat = self.total_price_in_vat - self.total_price_ex_vat
        return vat
