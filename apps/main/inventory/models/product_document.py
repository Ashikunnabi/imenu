from django.db import models

from apps.core.rbac.models import BaseModel
from apps.main.inventory.constants import ProductDocumentTypes

from .document import Document
from .product import Product


class ProductDocument(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="documents"
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    type = models.CharField(
        choices=ProductDocumentTypes.CHOICES, default=ProductDocumentTypes.IMAGE, max_length=50
    )

    def __str__(self):
        return f"{self.product}"
