from __future__ import annotations

import tempfile
from pathlib import Path

from django.test import TestCase, override_settings
from PIL import Image

from base.signals import DEFAULT_SITE_MEDIA_IMAGES, create_default_site_media


class TestCreateDefaultSiteMedia(TestCase):
    def test_creates_placeholder_images_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            create_default_site_media()

            for filename, (size, _) in DEFAULT_SITE_MEDIA_IMAGES.items():
                with Image.open(Path(media_root) / "site" / filename) as image:
                    self.assertEqual(image.size, size)

    def test_does_not_overwrite_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            existing_file = Path(media_root) / "site" / "background.jpg"
            existing_file.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (1, 1), color="red").save(existing_file, format="JPEG")

            create_default_site_media()

            with Image.open(existing_file) as image:
                self.assertEqual(image.size, (1, 1))

    def test_moves_legacy_images_into_site_directory(self) -> None:
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            legacy_file = Path(media_root) / "background.jpg"
            Image.new("RGB", (1, 1), color="red").save(legacy_file, format="JPEG")

            create_default_site_media()

            self.assertFalse(legacy_file.exists())
            with Image.open(Path(media_root) / "site" / "background.jpg") as image:
                self.assertEqual(image.size, (1, 1))
