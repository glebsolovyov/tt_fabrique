from django.db import models

class MailingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('client_filter')