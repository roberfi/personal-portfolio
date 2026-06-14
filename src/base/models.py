from __future__ import annotations

import mimetypes
from functools import cached_property

from django.db import models
from django_cooco.models import CookieGroup
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize
from solo.models import SingletonModel


class LegalAndPrivacy(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self) -> str:
        return self.title

    @cached_property
    def modal_name(self) -> str:
        return f"legal_and_privacy_{self.id}_modal"


class FollowMeLink(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()
    svg_view_box = models.CharField(max_length=16)
    svg_path = models.TextField()

    def __str__(self) -> str:
        return self.name


class GoogleAnalytics(SingletonModel):
    use_analytics = models.BooleanField(default=False)
    gtag = models.CharField(max_length=20, blank=True)
    cookie_consent = models.ForeignKey(CookieGroup, on_delete=models.RESTRICT, null=True)
    debug_mode = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Google Analytics"


class SiteMedia(SingletonModel):
    background_image = models.ImageField(
        upload_to="site/",
        default="site/background.jpg",
        help_text="Recommended aspect ratio as close as possible to 16:9, with a minimum size of "
        "1920x1080px. Also used, cropped to 1200x630 for the Open Graph preview and 1200x675 for "
        "the Twitter preview.",
    )
    background_image_display = ImageSpecField(
        source="background_image",
        processors=[ResizeToFit(1920, 1080, upscale=False)],
        format="JPEG",
        options={"quality": 85},
    )

    og_preview_image_display = ImageSpecField(
        source="background_image",
        processors=[SmartResize(1200, 630)],
        format="JPEG",
        options={"quality": 85},
    )

    twitter_preview_image_display = ImageSpecField(
        source="background_image",
        processors=[SmartResize(1200, 675)],
        format="JPEG",
        options={"quality": 85},
    )

    favicon = models.ImageField(upload_to="site/", default="site/favicon.ico")

    logo = models.ImageField(upload_to="site/", default="site/icon.png")
    logo_display = ImageSpecField(
        source="logo",
        processors=[ResizeToFit(64, 64, upscale=False)],
        format="PNG",
        options={"optimize": True},
    )

    def __str__(self) -> str:
        return "Site Media"

    @property
    def favicon_content_type(self) -> str:
        """Return the MIME type of the favicon, used for the favicon link tag."""
        return mimetypes.guess_type(self.favicon.name)[0] or "image/x-icon"
