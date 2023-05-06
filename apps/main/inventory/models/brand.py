from django.db import models

from apps.core.rbac.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15, blank=True, default="")
    url = models.URLField(blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.TextField(default="")
    tagline = models.TextField(default="")

    def __str__(self):
        return self.name
