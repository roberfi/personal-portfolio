"""Base test class for contact views."""

from __future__ import annotations

from utils.test_utils.base_view_test_case import BaseViewTestCase


class BaseContactViewTest(BaseViewTestCase):
    """Base class for testing contact view content."""

    @classmethod
    def init_db(cls) -> None:
        """Initialize database - no specific data needed for contact page."""
        pass
