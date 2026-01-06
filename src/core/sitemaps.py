"""Sitemap configuration for the portfolio website."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

if TYPE_CHECKING:
    from typing import Iterable


class StaticViewSitemap(Sitemap[str]):
    """Sitemap for static pages with multilanguage support."""

    priority = 1.0
    changefreq = "monthly"
    protocol = "https"
    i18n = True

    def items(self) -> Iterable[str]:
        """Return list of URL names to include in sitemap."""
        return (
            "home",
            "my-career",
        )

    def location(self, item: str) -> str:
        """Return the URL path for the given item."""
        return reverse(item)
