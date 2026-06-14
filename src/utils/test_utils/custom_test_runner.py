from __future__ import annotations

import logging
from typing import Any
from unittest import TestLoader
from unittest.suite import TestSuite

from django.test.runner import DiscoverRunner

# Loggers used in the contact flow: silenced during tests to avoid noise from the
# error paths under test. `assertLogs` overrides the level for its block, so tests
# asserting on these loggers are unaffected.
SILENCED_LOGGERS = ("contact", "recaptcha", "security")


class CustomTestLoader(TestLoader):
    def loadTestsFromTestCase(self, *args: Any, **kwargs: Any) -> TestSuite:  # noqa: N802 # Overrided method
        return TestSuite(
            test
            for test in super().loadTestsFromTestCase(*args, **kwargs)
            if test.__class__.__name__.startswith("Test")
        )


class CustomTestRunner(DiscoverRunner):
    test_loader = CustomTestLoader()

    def setup_test_environment(self, **kwargs: Any) -> None:
        super().setup_test_environment(**kwargs)

        for logger_name in SILENCED_LOGGERS:
            logging.getLogger(logger_name).setLevel(logging.CRITICAL)
