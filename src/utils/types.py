from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from django.utils.safestring import SafeString


class PageMetadata(TypedDict):
    """Metadata for a page used for SEO purposes."""

    page_title: str
    page_description: str
    page_keywords: str
    json_ld: SafeString
