import datetime
import uuid

from auditlog.models import AuditlogHistoryField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        help_text="This will be exposed to the outside world.",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)
    is_soft_deleted = models.BooleanField(default=False)
    soft_deleted_at = models.DateTimeField(blank=True, null=True)
    history = AuditlogHistoryField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set added_by during the first save.
            try:
                # exposed_request comes from RequestExposerMiddleware
                self.created_by = exposed_request.user
            except Exception:
                self.created_by_id = 1  # Request from management command
            self.updated_by = self.created_by
        else:
            try:
                self.updated_by = exposed_request.user
            except Exception:
                self.updated_by_id = 1  # Request from management command

            if self.is_soft_deleted:
                self.soft_deleted_at = datetime.datetime.now()
        super().save(*args, **kwargs)
