from __future__ import annotations

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .signals import create_default_site_media


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "base"

    def ready(self) -> None:
        post_migrate.connect(create_default_site_media, sender=self)
