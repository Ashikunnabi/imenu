from django.db import models

from apps.rbac.models import BaseModel


class Menu(BaseModel):
    name = models.CharField(max_length=256)
    type = models.ForeignKey(
        to="menu.MenuType",
        related_name="menus",
        on_delete=models.CASCADE,
        verbose_name="Menu type",
        help_text="Type of the menu",
    )
    start_at = models.DateTimeField(blank=True)
    end_at = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"], name="unique_menu_name_type"
            )
        ]

    def __str__(self):
        return f"{self.type} - {self.name}"
