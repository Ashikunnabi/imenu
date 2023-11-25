from django.db import models
from django.contrib.auth import get_user_model

from apps.rbac.models import BaseModel

User = get_user_model()


class Order(BaseModel):
    placed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_price_in_vat = models.DecimalField(decimal_places=6, max_digits=18)
    total_price_ex_vat = models.DecimalField(decimal_places=6, max_digits=18)
    vat = models.DecimalField(decimal_places=6, max_digits=18)
    # def __str__(self):
    #     return self.user.name

    def created_date(self):
        return self.created_at.strftime("%B %d, %Y")
