from django.db import models

from apps.rbac.models import BaseModel


class Table(BaseModel):
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
