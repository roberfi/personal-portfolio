"""Tests for structured logging in the contact view.

Log messages are not localized, so these tests don't need English/Spanish variants.
"""

from __future__ import annotations

import logging
from typing import Any, ContextManager, cast
from unittest import mock

import requests
from django.test import override_settings

import contact.tests.test_views.utils.constants as test_view_constants
from contact.models import ContactMessage
from contact.tests.test_views.base_view_test import BaseContactViewTest
from utils.test_utils.constants import Language


class _LogRecordWithExtra(logging.LogRecord):
    """A LogRecord with the extra fields set via `extra=` in the contact views, for typed access in tests."""

    contact_message_id: int
    recaptcha_score: float | None
    score: float
    success: bool
    action: str


def _get_form_data(*, with_recaptcha_token: bool = False) -> dict[str, str]:
    data = {
        "name": test_view_constants.TEST_NAME,
        "email": test_view_constants.TEST_EMAIL,
        "subject": test_view_constants.TEST_SUBJECT,
        "message": test_view_constants.TEST_MESSAGE,
    }

    if with_recaptcha_token:
        data["recaptcha_token"] = "test_token_12345"

    return data


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class TestContactLogging(BaseContactViewTest):
    """Test structured logging of contact form submissions."""

    request_path = "contact/"
    language = Language.ENGLISH

    def test_successful_submission_is_logged(self) -> None:
        """A successful submission logs an info message to the 'contact' logger."""
        with self.assertLogs("contact", level="INFO") as captured:
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data())

        message = ContactMessage.objects.get()

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        record = cast("_LogRecordWithExtra", captured.records[0])
        self.assertEqual(
            log_message := record.getMessage(),
            expected_message := "Contact form submission received",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )
        self.assertEqual(
            record.contact_message_id,
            message.pk,
            f"Expected contact_message_id '{message.pk}', got '{record.contact_message_id}'",
        )
        self.assertIsNone(
            record.recaptcha_score, f"Expected recaptcha_score to be None, got '{record.recaptcha_score}'"
        )

    def test_email_sending_failure_is_logged(self) -> None:
        """A failure sending the notification email logs an exception to the 'contact' logger."""
        with (
            mock.patch(
                "contact.views.EmailMessage.send", side_effect=Exception(test_view_constants.MOCKED_ERROR_MESSAGE)
            ),
            self.assertLogs("contact", level="ERROR") as captured,
        ):
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data())

        message = ContactMessage.objects.get()

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        record = cast("_LogRecordWithExtra", captured.records[0])
        self.assertEqual(
            log_message := record.getMessage(),
            expected_message := "Failed to send email notification for contact message",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )
        self.assertEqual(
            record.contact_message_id,
            message.pk,
            f"Expected contact_message_id '{message.pk}', got '{record.contact_message_id}'",
        )
        self.assertEqual(record.levelname, "ERROR", f"Expected log level 'ERROR', got '{record.levelname}'")


@override_settings(
    IS_RECAPTCHA_CONFIGURED=True,
    RECAPTCHA_SITE_KEY="test_site_key_12345",
    RECAPTCHA_SECRET_KEY="test_secret_key_67890",
    RECAPTCHA_SCORE_THRESHOLD=0.5,
)
class TestRecaptchaLogging(BaseContactViewTest):
    """Test structured logging of reCAPTCHA verification."""

    request_path = "contact/"
    language = Language.ENGLISH

    @staticmethod
    def _mock_recaptcha_response(*, success: bool, score: float, action: str) -> ContextManager[Any]:
        mock_response = mock.Mock(["raise_for_status", "json"])
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": success, "score": score, "action": action}
        return mock.patch("contact.views.requests.post", return_value=mock_response)

    def test_missing_token_is_logged_as_security_warning(self) -> None:
        """A submission missing the reCAPTCHA token logs a warning to the 'security' logger."""
        with self.assertLogs("security", level="WARNING") as captured:
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data())

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        self.assertEqual(
            log_message := captured.records[0].getMessage(),
            expected_message := "reCAPTCHA token missing from contact form submission",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )

    def test_successful_verification_is_logged(self) -> None:
        """A successful reCAPTCHA verification logs an info message to the 'recaptcha' logger with the score."""
        with (
            self._mock_recaptcha_response(success=True, score=0.9, action="contact_form"),
            self.assertLogs("recaptcha", level="INFO") as captured,
        ):
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data(with_recaptcha_token=True))

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        record = cast("_LogRecordWithExtra", captured.records[0])
        self.assertEqual(
            log_message := record.getMessage(),
            expected_message := "reCAPTCHA verification passed",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )
        self.assertEqual(score := record.score, 0.9, f"Expected score 0.9, got '{score}'")

    def test_low_score_is_logged_as_security_warning(self) -> None:
        """A reCAPTCHA verification with a score below the threshold logs a warning to the 'security' logger."""
        with (
            self._mock_recaptcha_response(success=True, score=0.3, action="contact_form"),
            self.assertLogs("security", level="WARNING") as captured,
        ):
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data(with_recaptcha_token=True))

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        record = cast("_LogRecordWithExtra", captured.records[0])
        self.assertEqual(
            log_message := record.getMessage(),
            expected_message := "reCAPTCHA verification failed",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )
        self.assertTrue(record.success, f"Expected success to be True, got '{record.success}'")
        self.assertEqual(score := record.score, 0.3, f"Expected score 0.3, got '{score}'")
        self.assertEqual(action := record.action, "contact_form", f"Expected action 'contact_form', got '{action}'")

    def test_network_error_is_logged_as_recaptcha_warning(self) -> None:
        """A network error contacting the reCAPTCHA API logs a warning to the 'recaptcha' logger."""
        with (
            mock.patch("contact.views.requests.post", side_effect=requests.RequestException("Network error")),
            self.assertLogs("recaptcha", level="WARNING") as captured,
        ):
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data(with_recaptcha_token=True))

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        self.assertEqual(
            log_message := captured.records[0].getMessage(),
            expected_message := "reCAPTCHA API error, allowing submission",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )

    def test_unexpected_error_is_logged_as_recaptcha_error(self) -> None:
        """An unexpected error during reCAPTCHA verification logs an exception to the 'recaptcha' logger."""
        with (
            mock.patch("contact.views.requests.post", side_effect=ValueError("Unexpected error")),
            self.assertLogs("recaptcha", level="ERROR") as captured,
        ):
            self.client.post(f"/{self.language}/{self.request_path}", data=_get_form_data(with_recaptcha_token=True))

        self.assertEqual(
            records_len := len(captured.records), 1, f"Expected exactly one log record, got '{records_len}'"
        )
        record = captured.records[0]
        self.assertEqual(
            log_message := record.getMessage(),
            expected_message := "Unexpected error during reCAPTCHA verification",
            f"Expected log message '{expected_message}', got '{log_message}'",
        )
        self.assertEqual(record.levelname, "ERROR", f"Expected log level 'ERROR', got '{record.levelname}'")
