from __future__ import annotations

from typing import Any
from unittest import TestLoader
from unittest.suite import TestSuite

from django.test.runner import DiscoverRunner


class CustomTestLoader(TestLoader):
    def loadTestsFromTestCase(self, *args: Any, **kwargs: Any) -> TestSuite:  # noqa: N802 # Overrided method
        return TestSuite(
            test
            for test in super().loadTestsFromTestCase(*args, **kwargs)
            if test.__class__.__name__.startswith("Test")
        )


class CustomTestRunner(DiscoverRunner):
    test_loader = CustomTestLoader()
