from __future__ import annotations

from django.db import models
from solo.models import SingletonModel

from base.models import LegalAndPrivacy


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


class ContactPrivacyNotice(SingletonModel):
    """Configures which Legal and Privacy section is used as the contact form's privacy policy."""

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
        return "Contact Privacy Notice"
