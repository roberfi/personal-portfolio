from __future__ import annotations

from io import BytesIO
from typing import ClassVar

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from base.models import SiteMedia


def _build_uploaded_image(name: str, size: tuple[int, int], image_format: str) -> SimpleUploadedFile:
    buffer = BytesIO()
    Image.new("RGB", size, color="red").save(buffer, format=image_format)

    return SimpleUploadedFile(name, buffer.getvalue(), content_type=f"image/{image_format.lower()}")


class TestSiteMediaModelDefaults(TestCase):
    site_media: ClassVar[SiteMedia]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.site_media = SiteMedia.get_solo()

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.site_media),
            expected_str := "Site Media",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_default_field_values(self) -> None:
        self.assertEqual(self.site_media.background_image.url, "/media/site/background.jpg")
        self.assertEqual(self.site_media.favicon.url, "/media/site/favicon.ico")
        self.assertEqual(self.site_media.logo.url, "/media/site/icon.png")

    def test_favicon_content_type_for_ico_file(self) -> None:
        self.assertEqual(self.site_media.favicon_content_type, "image/vnd.microsoft.icon")

    def test_favicon_content_type_fallback_for_unknown_extension(self) -> None:
        self.site_media.favicon = "site/favicon.unknownext"
        self.assertEqual(self.site_media.favicon_content_type, "image/x-icon")


class TestSiteMediaModelDisplayFields(TestCase):
    def test_background_image_display_is_resized_to_fit(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.background_image = _build_uploaded_image("background.jpg", (3840, 2160), "JPEG")
        site_media.save()

        with Image.open(site_media.background_image_display.path) as image:
            self.assertEqual(image.size, (1920, 1080))

    def test_og_preview_image_display_is_resized_to_fill(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.background_image = _build_uploaded_image("background.jpg", (3000, 1000), "JPEG")
        site_media.save()

        with Image.open(site_media.og_preview_image_display.path) as image:
            self.assertEqual(image.size, (1200, 630))

    def test_twitter_preview_image_display_is_resized_to_fill(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.background_image = _build_uploaded_image("background.jpg", (3000, 1000), "JPEG")
        site_media.save()

        with Image.open(site_media.twitter_preview_image_display.path) as image:
            self.assertEqual(image.size, (1200, 675))

    def test_logo_display_is_resized_to_fit(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.logo = _build_uploaded_image("logo.png", (512, 512), "PNG")
        site_media.save()

        with Image.open(site_media.logo_display.path) as image:
            self.assertEqual(image.size, (64, 64))

    def test_small_images_are_not_upscaled(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.logo = _build_uploaded_image("small_logo.png", (32, 32), "PNG")
        site_media.save()

        with Image.open(site_media.logo_display.path) as image:
            self.assertEqual(image.size, (32, 32))
