from __future__ import annotations

from django.contrib.admin import ModelAdmin, register

from .models import ContactMessage


@register(ContactMessage)
class ContactMessageAdmin(ModelAdmin[ContactMessage]):
    """Admin interface for ContactMessage model."""

    readonly_fields = (
        "name",
        "email",
        "subject",
        "created_at",
        "message",
        "error",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    date_hierarchy = "created_at"
