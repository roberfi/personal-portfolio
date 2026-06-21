from __future__ import annotations

from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy
from solo.admin import SingletonModelAdmin

from .forms import ContactFormConfigurationForm
from .models import ContactFormConfiguration, ContactMessage


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
        "recaptcha_score",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    date_hierarchy = "created_at"


@register(ContactFormConfiguration)
class ContactFormConfigurationAdmin(SingletonModelAdmin):
    """Admin interface for ContactFormConfiguration singleton model."""

    form = ContactFormConfigurationForm

    fieldsets = (
        (None, {"fields": ("email_provider", "default_from_email", "contact_email")}),
        (
            gettext_lazy("SMTP settings"),
            {
                "classes": ("email-config-smtp",),
                "fields": (
                    "smtp_host",
                    "smtp_port",
                    "smtp_use_tls",
                    "smtp_use_ssl",
                    "smtp_username",
                    "smtp_password",
                    "smtp_timeout",
                ),
            },
        ),
        (
            gettext_lazy("Brevo API settings"),
            {
                "classes": ("email-config-brevo_api",),
                "fields": ("brevo_api_key",),
            },
        ),
        (gettext_lazy("Contact page"), {"fields": ("intro_es", "intro_en")}),
        (gettext_lazy("Privacy notice"), {"fields": ("legal_and_privacy",)}),
    )

    class Media:
        js = ("contact/admin/email_configuration.js",)
