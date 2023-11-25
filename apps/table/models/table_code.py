from django.contrib.auth import get_user_model
from django.db import models
from apps.base.validators import ScreenMethodValidator

from apps.rbac.models import BaseModel

from ..constants import TableCodeTypes
from .table import Table

User = get_user_model()


class TableCode(BaseModel):
    validators = [ScreenMethodValidator]

    type = models.CharField(
        choices=TableCodeTypes.CHOICES, default=TableCodeTypes.UPC, max_length=256
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="codes")
    value = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["table", "type"], name="unique_table_type")
        ]

    def __str__(self):
        return self.type

    def screen_unique_table_and_type(self):
        if (
            self.__class__.objects.filter(table=self.table, type=self.type)
            .exclude(id=self.id)
            .exists()
        ):
            return "Table code with this table and type already exists."
