from django.db import models

from apps.core.rbac.models import BaseModel


class Group(BaseModel):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subgroups",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "name"], name="unique_group_code_name"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
