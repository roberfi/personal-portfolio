from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.test import TestCase

from contact.email_backend import DatabaseEmailBackend
from contact.models import ContactFormConfiguration, EmailProvider

if TYPE_CHECKING:
    from anymail.backends.brevo import EmailBackend as BrevoEmailBackend
    from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class TestDatabaseEmailBackend(TestCase):
    """Test cases for DatabaseEmailBackend."""

    def setUp(self) -> None:
        self.backend = DatabaseEmailBackend()

    def test_build_backend_for_smtp(self) -> None:
        """Test that an SMTP backend is built with the configured provider_config values."""
        config = ContactFormConfiguration.get_solo()
        config.email_provider = EmailProvider.SMTP
        config.provider_config = {
            "host": "smtp.example.com",
            "port": 2525,
            "username": "user",
            "password": "pass",
            "use_tls": False,
            "use_ssl": True,
            "timeout": 15,
        }

        smtp_backend = cast("SMTPEmailBackend", self.backend._build_backend(config))

        self.assertEqual(
            smtp_backend.host, "smtp.example.com", f"Expected host 'smtp.example.com', got '{smtp_backend.host}'"
        )
        self.assertEqual(smtp_backend.port, 2525, f"Expected port 2525, got '{smtp_backend.port}'")
        self.assertEqual(smtp_backend.username, "user", f"Expected username 'user', got '{smtp_backend.username}'")
        self.assertEqual(smtp_backend.password, "pass", f"Expected password 'pass', got '{smtp_backend.password}'")
        self.assertFalse(smtp_backend.use_tls, f"Expected use_tls False, got '{smtp_backend.use_tls}'")
        self.assertTrue(smtp_backend.use_ssl, f"Expected use_ssl True, got '{smtp_backend.use_ssl}'")
        self.assertEqual(smtp_backend.timeout, 15, f"Expected timeout 15, got '{smtp_backend.timeout}'")

    def test_build_backend_for_smtp_defaults(self) -> None:
        """Test that an SMTP backend falls back to sensible defaults when provider_config is empty."""
        config = ContactFormConfiguration.get_solo()
        config.email_provider = EmailProvider.SMTP
        config.provider_config = {}

        smtp_backend = cast("SMTPEmailBackend", self.backend._build_backend(config))

        self.assertEqual(
            smtp_backend.host, "localhost", f"Expected default host 'localhost', got '{smtp_backend.host}'"
        )
        self.assertEqual(smtp_backend.port, 587, f"Expected default port 587, got '{smtp_backend.port}'")
        self.assertFalse(smtp_backend.username, f"Expected empty default username, got '{smtp_backend.username}'")
        self.assertFalse(smtp_backend.password, f"Expected empty default password, got '{smtp_backend.password}'")
        self.assertTrue(smtp_backend.use_tls, f"Expected default use_tls True, got '{smtp_backend.use_tls}'")
        self.assertFalse(smtp_backend.use_ssl, f"Expected default use_ssl False, got '{smtp_backend.use_ssl}'")
        self.assertEqual(smtp_backend.timeout, 10, f"Expected default timeout 10, got '{smtp_backend.timeout}'")

    def test_build_backend_for_brevo_api(self) -> None:
        """Test that a Brevo API backend is built with the configured API key."""
        config = ContactFormConfiguration.get_solo()
        config.email_provider = EmailProvider.BREVO_API
        config.provider_config = {"api_key": "test-api-key"}

        brevo_backend = cast("BrevoEmailBackend", self.backend._build_backend(config))

        self.assertEqual(
            brevo_backend.api_key, "test-api-key", f"Expected api_key 'test-api-key', got '{brevo_backend.api_key}'"
        )
