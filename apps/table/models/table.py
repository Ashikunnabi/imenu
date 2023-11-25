from django.db import models
from apps.base.validators import ScreenMethodValidator

from apps.rbac.models import BaseModel


class Table(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)
    type = models.ForeignKey(
        to="table.TableType",
        related_name="tables",
        on_delete=models.CASCADE,
        verbose_name="Table type",
        help_text="Type of the table",
    )
    start_at = models.DateTimeField(blank=True)
    end_at = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"], name="unique_table_name_type"
            )
        ]

    def __str__(self):
        return f"{self.type} - {self.name}"

    def screen_unique_name_and_type(self):
        if self.__class__.objects.filter(name=self.name, type=self.type).exclude(id=self.id).exists():
            return "Table with this name and type already exists."
