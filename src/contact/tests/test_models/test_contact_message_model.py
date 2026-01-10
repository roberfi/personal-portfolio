"""Tests for ContactMessage model."""

from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from contact.models import ContactMessage

# Constants
TEST_NAME_1 = "Test Name 1"
TEST_EMAIL_1 = "test1@example.com"
TEST_SUBJECT_1 = "Test Subject 1"
TEST_MESSAGE_1 = "Test message content 1"

TEST_NAME_2 = "Test Name 2"
TEST_EMAIL_2 = "test2@example.com"
TEST_SUBJECT_2 = "Test Subject 2"
TEST_MESSAGE_2 = "Test message content 2"


class TestContactMessageModel(TestCase):
    """Test cases for the ContactMessage model."""

    message1: ClassVar[ContactMessage]
    message2: ClassVar[ContactMessage]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.message1 = ContactMessage.objects.create(
            name=TEST_NAME_1,
            email=TEST_EMAIL_1,
            subject=TEST_SUBJECT_1,
            message=TEST_MESSAGE_1,
        )
        cls.message2 = ContactMessage.objects.create(
            name=TEST_NAME_2,
            email=TEST_EMAIL_2,
            subject=TEST_SUBJECT_2,
            message=TEST_MESSAGE_2,
        )

    def test_str(self) -> None:
        """Test the string representation of ContactMessage."""
        self.assertEqual(
            returned_str := str(self.message1),
            expected_str := f"{TEST_NAME_1} - {TEST_SUBJECT_1}",
            f"The __str__ method is returning '{returned_str}' instead of expected value '{expected_str}'",
        )

    def test_default_is_read(self) -> None:
        """Test that is_read defaults to False."""
        self.assertFalse(self.message1.is_read)

    def test_created_at_auto_set(self) -> None:
        """Test that created_at is automatically set."""
        self.assertIsNotNone(self.message1.created_at)

    def test_error_field(self) -> None:
        """Test the error field functionality."""
        self.assertEqual(self.message1.error, "", "The error field should be an empty string by default")

        self.message1.error = "Sample error message"
        self.message1.save()
        self.message1.refresh_from_db()

        self.assertEqual(self.message1.error, "Sample error message", "The error field did not update correctly")

    def test_ordering(self) -> None:
        """Test that messages are ordered by created_at descending."""
        ordered_messages = list(ContactMessage.objects.all())
        self.assertEqual(
            ordered_messages,
            [self.message2, self.message1],
            "The messages are not ordered by created_at descending as expected",
        )
