from __future__ import annotations

import logging
import shutil
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any
from unittest import TestLoader
from unittest.suite import TestSuite

from django.conf import settings
from django.test.runner import DiscoverRunner
from PIL import Image

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
    _original_media_root: Path
    _media_root: Path

    def setup_test_environment(self, **kwargs: Any) -> None:
        super().setup_test_environment(**kwargs)

        for logger_name in SILENCED_LOGGERS:
            logging.getLogger(logger_name).setLevel(logging.CRITICAL)

        self._original_media_root = settings.MEDIA_ROOT
        self._media_root = Path(tempfile.mkdtemp(prefix="test-media-"))
        settings.MEDIA_ROOT = self._media_root

        site_dir = self._media_root / "site"
        site_dir.mkdir(parents=True, exist_ok=True)
        buffer = BytesIO()
        Image.new("RGB", (1920, 1080), color=(60, 68, 80)).save(buffer, format="PNG")
        (site_dir / "portrait.png").write_bytes(buffer.getvalue())

    def teardown_test_environment(self, **kwargs: Any) -> None:
        settings.MEDIA_ROOT = self._original_media_root
        shutil.rmtree(self._media_root, ignore_errors=True)

        super().teardown_test_environment(**kwargs)
