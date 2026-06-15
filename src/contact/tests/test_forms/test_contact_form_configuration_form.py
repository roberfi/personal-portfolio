from __future__ import annotations

from django.test import TestCase

from contact.forms import ContactFormConfigurationForm
from contact.models import ContactFormConfiguration, EmailProvider


class TestContactFormConfigurationForm(TestCase):
    """Test cases for ContactFormConfigurationForm."""

    def _build_form_data(self, **overrides: object) -> dict[str, object]:
        data: dict[str, object] = {
            "email_provider": EmailProvider.SMTP,
            "default_from_email": "noreply@example.com",
            "contact_email": "contact@example.com",
        }
        data.update(overrides)
        return data

    def test_smtp_requires_host(self) -> None:
        """Test that SMTP provider requires a host to be set."""
        form = ContactFormConfigurationForm(
            data=self._build_form_data(email_provider=EmailProvider.SMTP, smtp_host=""),
            instance=ContactFormConfiguration.get_solo(),
        )

        self.assertFalse(
            form.is_valid(), "The form should be invalid when email_provider is SMTP and smtp_host is empty"
        )
        self.assertIn("smtp_host", form.errors, f"Expected a 'smtp_host' error, got errors: {form.errors}")

    def test_brevo_api_requires_api_key(self) -> None:
        """Test that Brevo API provider requires an API key to be set."""
        form = ContactFormConfigurationForm(
            data=self._build_form_data(email_provider=EmailProvider.BREVO_API, brevo_api_key=""),
            instance=ContactFormConfiguration.get_solo(),
        )

        self.assertFalse(
            form.is_valid(), "The form should be invalid when email_provider is Brevo API and brevo_api_key is empty"
        )
        self.assertIn("brevo_api_key", form.errors, f"Expected a 'brevo_api_key' error, got errors: {form.errors}")

    def test_save_smtp_provider_config(self) -> None:
        """Test that saving with the SMTP provider assembles provider_config from the smtp_* fields."""
        form = ContactFormConfigurationForm(
            data=self._build_form_data(
                email_provider=EmailProvider.SMTP,
                smtp_host="smtp.example.com",
                smtp_port=2525,
                smtp_use_tls=False,
                smtp_use_ssl=True,
                smtp_username="user",
                smtp_password="pass",
                smtp_timeout=15,
            ),
            instance=ContactFormConfiguration.get_solo(),
        )

        self.assertTrue(form.is_valid(), f"Expected the form to be valid, got errors: {form.errors}")
        instance = form.save()

        self.assertEqual(
            instance.provider_config,
            expected_config := {
                "host": "smtp.example.com",
                "port": 2525,
                "use_tls": False,
                "use_ssl": True,
                "username": "user",
                "password": "pass",
                "timeout": 15,
            },
            f"Expected provider_config '{expected_config}', got '{instance.provider_config}'",
        )

    def test_save_brevo_api_provider_config(self) -> None:
        """Test that saving with the Brevo API provider assembles provider_config from the brevo_api_key field."""
        form = ContactFormConfigurationForm(
            data=self._build_form_data(email_provider=EmailProvider.BREVO_API, brevo_api_key="test-api-key"),
            instance=ContactFormConfiguration.get_solo(),
        )

        self.assertTrue(form.is_valid(), f"Expected the form to be valid, got errors: {form.errors}")
        instance = form.save()

        self.assertEqual(
            instance.provider_config,
            expected_config := {"api_key": "test-api-key"},
            f"Expected provider_config '{expected_config}', got '{instance.provider_config}'",
        )

    def test_initial_values_from_existing_provider_config(self) -> None:
        """Test that the form's extra fields are pre-filled from the instance's provider_config."""
        config = ContactFormConfiguration.get_solo()
        config.provider_config = {"host": "smtp.example.com", "port": 2525, "api_key": "test-api-key"}
        config.save()

        form = ContactFormConfigurationForm(instance=config)

        self.assertEqual(
            smtp_host_initial := form.fields["smtp_host"].initial,
            "smtp.example.com",
            f"Expected smtp_host initial 'smtp.example.com', got '{smtp_host_initial}'",
        )
        self.assertEqual(
            smtp_port_initial := form.fields["smtp_port"].initial,
            2525,
            f"Expected smtp_port initial 2525, got '{smtp_port_initial}'",
        )
        self.assertEqual(
            brevo_api_key_initial := form.fields["brevo_api_key"].initial,
            "test-api-key",
            f"Expected brevo_api_key initial 'test-api-key', got '{brevo_api_key_initial}'",
        )
