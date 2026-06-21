from __future__ import annotations

from django.db import models
from solo.models import SingletonModel

from base.models import LegalAndPrivacy
from utils.fields import EncryptedJSONField


class EmailProvider(models.TextChoices):
    """Available email providers for sending the contact form notification."""

    SMTP = "smtp", "SMTP"
    BREVO_API = "brevo_api", "Brevo API"


class ContactMessage(models.Model):
    """Model to store contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    error = models.TextField(blank=True)
    recaptcha_score = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"


class ContactFormConfiguration(SingletonModel):
    """Singleton configuration for the contact form: privacy notice and email sending."""

    email_provider = models.CharField(max_length=20, choices=EmailProvider.choices, default=EmailProvider.SMTP)
    default_from_email = models.EmailField(default="noreply@localhost")
    contact_email = models.EmailField(default="contact@localhost")
    provider_config = EncryptedJSONField(
        default=dict,
        blank=True,
        help_text="Provider-specific settings, encrypted at rest. For SMTP: host, port, use_tls, "
        "use_ssl, username, password, timeout. For Brevo API: api_key.",
    )

    intro = models.TextField(
        blank=True,
        help_text="Text shown above the contact form. Leave empty to use the default.",
    )

    legal_and_privacy = models.ForeignKey(
        LegalAndPrivacy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Legal and Privacy section used as the contact form's privacy policy. "
        "If empty, no consent checkbox is shown.",
    )

    def __str__(self) -> str:
        return "Contact Form Configuration"
