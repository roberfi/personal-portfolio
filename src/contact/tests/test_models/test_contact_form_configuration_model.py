"""Tests for ContactFormConfiguration model."""

from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from contact.models import ContactFormConfiguration, EmailProvider


class TestContactFormConfigurationModel(TestCase):
    """Test cases for the ContactFormConfiguration model."""

    contact_form_configuration: ClassVar[ContactFormConfiguration]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.contact_form_configuration = ContactFormConfiguration.get_solo()

    def test_str(self) -> None:
        """Test the string representation of ContactFormConfiguration."""
        self.assertEqual(
            returned_str := str(self.contact_form_configuration),
            expected_str := "Contact Form Configuration",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_default_field_values(self) -> None:
        """Test the default values of the ContactFormConfiguration fields."""
        self.assertIsNone(
            self.contact_form_configuration.legal_and_privacy,
            f"Expected legal_and_privacy to default to None, got '{self.contact_form_configuration.legal_and_privacy}'",
        )
        self.assertEqual(
            email_provider := self.contact_form_configuration.email_provider,
            EmailProvider.SMTP,
            f"Expected email_provider to default to '{EmailProvider.SMTP}', got '{email_provider}'",
        )
        self.assertEqual(
            default_from_email := self.contact_form_configuration.default_from_email,
            "noreply@localhost",
            f"Expected default_from_email to default to 'noreply@localhost', got '{default_from_email}'",
        )
        self.assertEqual(
            contact_email := self.contact_form_configuration.contact_email,
            "contact@localhost",
            f"Expected contact_email to default to 'contact@localhost', got '{contact_email}'",
        )
        self.assertEqual(
            provider_config := self.contact_form_configuration.provider_config,
            {},
            f"Expected provider_config to default to an empty dict, got '{provider_config}'",
        )

    def test_provider_config_round_trip(self) -> None:
        """Test that provider_config is encrypted at rest and decrypted transparently on read."""
        provider_config = {"host": "smtp.example.com", "port": 587, "password": "secret"}

        self.contact_form_configuration.provider_config = provider_config
        self.contact_form_configuration.save()

        reloaded = ContactFormConfiguration.objects.get(pk=self.contact_form_configuration.pk)
        self.assertEqual(
            reloaded.provider_config,
            provider_config,
            f"Expected provider_config '{provider_config}' to round-trip unchanged, got '{reloaded.provider_config}'",
        )
