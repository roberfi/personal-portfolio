from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from base.models import GoogleAnalytics


class TestGoogleAnalyticsModel(TestCase):
    google_analytics: ClassVar[GoogleAnalytics]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.google_analytics = GoogleAnalytics(use_analytics=True, gtag="G-1234567890")

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.google_analytics),
            expected_str := "Google Analytics",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
