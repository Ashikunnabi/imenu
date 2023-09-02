from django.db import models

from apps.inventory.models import Document
from apps.rbac.models import BaseModel

from ..constants import TableDocumentTypes
from .table import Table


class TableDocument(BaseModel):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="documents"
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    type = models.CharField(
        choices=TableDocumentTypes.CHOICES,
        default=TableDocumentTypes.IMAGE,
        max_length=50,
    )

    def __str__(self):
        return f"{self.table}"
