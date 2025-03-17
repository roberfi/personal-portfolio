from __future__ import annotations

from datetime import date
from typing import Self
from unittest import TestLoader
from unittest.suite import TestSuite

from django.test.runner import DiscoverRunner


class CustomTestLoader(TestLoader):
    def loadTestsFromTestCase(self, *args, **kwargs) -> TestSuite:  # noqa: N802 # Overrided method
        return TestSuite(
            test
            for test in super().loadTestsFromTestCase(*args, **kwargs)
            if test.__class__.__name__.startswith("Test")
        )


class CustomTestRunner(DiscoverRunner):
    test_loader = CustomTestLoader()


def get_date_with_mocked_today(today_date: date) -> type[date]:
    class MockedDate(date):
        @classmethod
        def today(cls) -> Self:
            return cls(today_date.year, today_date.month, today_date.day)

    return MockedDate
