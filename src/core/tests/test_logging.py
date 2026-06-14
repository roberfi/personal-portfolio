"""Tests for the structured logging configuration."""

from __future__ import annotations

import json
import logging
import sys

from django.test import SimpleTestCase

from core.logging import JsonFormatter


class TestJsonFormatter(SimpleTestCase):
    """Test the JsonFormatter used for structured production logging."""

    def setUp(self) -> None:
        self.formatter = JsonFormatter()

    def test_basic_fields(self) -> None:
        """The formatted output is valid JSON with the basic log fields."""
        record = logging.LogRecord(
            name="contact",
            level=logging.WARNING,
            pathname=__file__,
            lineno=1,
            msg="Hello world",
            args=None,
            exc_info=None,
        )

        data = json.loads(self.formatter.format(record))

        self.assertEqual(data["level"], "WARNING")
        self.assertEqual(data["logger"], "contact")
        self.assertEqual(data["message"], "Hello world")
        self.assertIn("timestamp", data)

    def test_extra_fields_are_included(self) -> None:
        """Fields passed via `extra=` are included in the JSON output."""
        record = logging.LogRecord(
            name="contact",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="Submission received",
            args=None,
            exc_info=None,
        )
        record.contact_message_id = 42
        record.recaptcha_score = 0.9

        data = json.loads(self.formatter.format(record))

        self.assertEqual(data["contact_message_id"], 42)
        self.assertEqual(data["recaptcha_score"], 0.9)

    def test_exception_info_is_included(self) -> None:
        """Exception information is included as a string under 'exception'."""
        try:
            error_message = "boom"
            raise ValueError(error_message)
        except ValueError:
            record = logging.LogRecord(
                name="contact",
                level=logging.ERROR,
                pathname=__file__,
                lineno=1,
                msg="Something failed",
                args=None,
                exc_info=sys.exc_info(),
            )

        data = json.loads(self.formatter.format(record))

        self.assertIn("exception", data)
        self.assertIn("ValueError: boom", data["exception"])
