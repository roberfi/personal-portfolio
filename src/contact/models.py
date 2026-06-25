from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy
from solo.models import SingletonModel

from base.models import LegalAndPrivacy
from utils.fields import EncryptedJSONField


class EmailProvider(models.TextChoices):
    """Available email providers for sending the contact form notification."""

    SMTP = "smtp", "SMTP"
    BREVO_API = "brevo_api", "Brevo API"


class BudgetRange(models.TextChoices):
    UNDER_1K = "under_1k", gettext_lazy("Under €1,000")
    BETWEEN_1K_5K = "1k_5k", gettext_lazy("€1,000 \u2013 €5,000")
    BETWEEN_5K_15K = "5k_15k", gettext_lazy("€5,000 \u2013 €15,000")
    OVER_15K = "over_15k", gettext_lazy("Over €15,000")


class Timeline(models.TextChoices):
    UNDER_1_MONTH = "under_1m", gettext_lazy("Less than 1 month")
    BETWEEN_1_3_MONTHS = "1m_3m", gettext_lazy("1 \u2013 3 months")
    BETWEEN_3_6_MONTHS = "3m_6m", gettext_lazy("3 \u2013 6 months")
    OVER_6_MONTHS = "over_6m", gettext_lazy("6+ months")


class ContactMessage(models.Model):
    """Model to store contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    service_interest = models.ForeignKey(
        "home.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_messages",
    )
    budget_range = models.CharField(max_length=20, choices=BudgetRange.choices, blank=True)
    timeline = models.CharField(max_length=20, choices=Timeline.choices, blank=True)
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
