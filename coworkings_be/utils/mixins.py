from django.db import models


class AuditMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    ast_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
