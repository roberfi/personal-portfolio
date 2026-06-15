from __future__ import annotations

from typing import TYPE_CHECKING, Any

from anymail.backends.brevo import EmailBackend as BrevoEmailBackend
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

from .models import ContactFormConfiguration, EmailProvider

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.core.mail.message import EmailMessage


class EmailProviderNotConfiguredError(Exception):
    pass


class DatabaseEmailBackend(BaseEmailBackend):
    """Email backend that delegates to SMTP or Brevo's API, configured via ContactFormConfiguration."""

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        config = ContactFormConfiguration.get_solo()
        return self._build_backend(config).send_messages(email_messages) or 0

    def _build_backend(self, config: ContactFormConfiguration) -> BaseEmailBackend:
        provider_config: dict[str, Any] = config.provider_config

        match config.email_provider:
            case EmailProvider.BREVO_API:
                return BrevoEmailBackend(  # type: ignore[no-any-return]
                    api_key=provider_config.get("api_key", ""),
                )

            case EmailProvider.SMTP:
                return SMTPEmailBackend(
                    host=provider_config.get("host", "localhost"),
                    port=provider_config.get("port", 587),
                    username=provider_config.get("username") or None,
                    password=provider_config.get("password") or None,
                    use_tls=provider_config.get("use_tls", True),
                    use_ssl=provider_config.get("use_ssl", False),
                    timeout=provider_config.get("timeout", 10),
                )

            case _:
                error_message = f"Email provider '{config.email_provider}' not configured"
                raise EmailProviderNotConfiguredError(error_message)
