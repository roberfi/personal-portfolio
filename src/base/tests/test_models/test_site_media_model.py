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
        self.assertEqual(
            background_url := self.site_media.portrait_image.url,
            "/media/site/portrait.png",
            f"Expected portrait_image.url to default to '/media/site/portrait.png', got '{background_url}'",
        )
        self.assertEqual(
            favicon_url := self.site_media.favicon.url,
            "/media/site/favicon.ico",
            f"Expected favicon.url to default to '/media/site/favicon.ico', got '{favicon_url}'",
        )
        self.assertEqual(
            logo_url := self.site_media.logo.url,
            "/media/site/icon.png",
            f"Expected logo.url to default to '/media/site/icon.png', got '{logo_url}'",
        )

    def test_favicon_content_type_for_ico_file(self) -> None:
        self.assertEqual(
            content_type := self.site_media.favicon_content_type,
            "image/vnd.microsoft.icon",
            f"Expected favicon_content_type 'image/vnd.microsoft.icon' for an .ico file, got '{content_type}'",
        )

    def test_favicon_content_type_fallback_for_unknown_extension(self) -> None:
        self.site_media.favicon = "site/favicon.unknownext"
        self.assertEqual(
            content_type := self.site_media.favicon_content_type,
            "image/x-icon",
            f"Expected favicon_content_type to fall back to 'image/x-icon' for an unknown extension, "
            f"got '{content_type}'",
        )


class TestSiteMediaModelDisplayFields(TestCase):
    def test_portrait_mobile_display_is_resized_to_fit(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.portrait_image = _build_uploaded_image("portrait.jpg", (1920, 1080), "JPEG")
        site_media.save()

        with Image.open(site_media.portrait_mobile_display.path) as image:
            self.assertLessEqual(
                image.size[0],
                900,
                f"Expected portrait_mobile_display width to be at most 900px, got '{image.size[0]}'",
            )
            self.assertLessEqual(
                image.size[1],
                506,
                f"Expected portrait_mobile_display height to be at most 506px, got '{image.size[1]}'",
            )

    def test_og_preview_image_display_is_resized_to_fill(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.portrait_image = _build_uploaded_image("background.jpg", (3000, 1000), "JPEG")
        site_media.save()

        with Image.open(site_media.og_preview_image_display.path) as image:
            self.assertEqual(
                image.size,
                expected_size := (1200, 630),
                f"Expected og_preview_image_display to be resized to '{expected_size}', got '{image.size}'",
            )

    def test_twitter_preview_image_display_is_resized_to_fill(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.portrait_image = _build_uploaded_image("background.jpg", (3000, 1000), "JPEG")
        site_media.save()

        with Image.open(site_media.twitter_preview_image_display.path) as image:
            self.assertEqual(
                image.size,
                expected_size := (1200, 675),
                f"Expected twitter_preview_image_display to be resized to '{expected_size}', got '{image.size}'",
            )

    def test_logo_display_is_resized_to_fit(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.logo = _build_uploaded_image("logo.png", (512, 512), "PNG")
        site_media.save()

        with Image.open(site_media.logo_display.path) as image:
            self.assertEqual(
                image.size,
                expected_size := (64, 64),
                f"Expected logo_display to be resized to '{expected_size}', got '{image.size}'",
            )

    def test_small_images_are_not_upscaled(self) -> None:
        site_media = SiteMedia.get_solo()
        site_media.logo = _build_uploaded_image("small_logo.png", (32, 32), "PNG")
        site_media.save()

        with Image.open(site_media.logo_display.path) as image:
            self.assertEqual(
                image.size,
                expected_size := (32, 32),
                f"Expected small logo_display to not be upscaled and stay '{expected_size}', got '{image.size}'",
            )
