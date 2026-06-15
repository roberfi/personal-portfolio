"""Tests for ContactPrivacyNotice model."""

from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from contact.models import ContactPrivacyNotice


class TestContactPrivacyNoticeModel(TestCase):
    """Test cases for the ContactPrivacyNotice model."""

    contact_privacy_notice: ClassVar[ContactPrivacyNotice]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.contact_privacy_notice = ContactPrivacyNotice.get_solo()

    def test_str(self) -> None:
        """Test the string representation of ContactPrivacyNotice."""
        self.assertEqual(
            returned_str := str(self.contact_privacy_notice),
            expected_str := "Contact Privacy Notice",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_default_field_values(self) -> None:
        """Test the default values of the ContactPrivacyNotice fields."""
        self.assertIsNone(self.contact_privacy_notice.legal_and_privacy)
