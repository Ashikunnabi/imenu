from django.contrib.auth import get_user_model
from django.db import models

from apps.rbac.models import BaseModel

from ..constants import TableCodeTypes
from .table import Table

User = get_user_model()


class TableCode(BaseModel):
    type = models.CharField(
        choices=TableCodeTypes.CHOICES, default=TableCodeTypes.UPC, max_length=256
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="codes")
    value = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["table", "type"], name="unique_table_type"
            )
        ]

    def __str__(self):
        return self.type
