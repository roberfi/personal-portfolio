from __future__ import annotations

from typing import TYPE_CHECKING

import markdown
from bs4 import BeautifulSoup
from django.conf import settings

if TYPE_CHECKING:
    from django.http import HttpRequest


def markdown_to_plaintext(text: str) -> str:
    """Convert markdown to plain text.

    Args:
        text: The markdown text to convert.

    Returns:
        The plain text representation of the markdown.
    """
    soup = BeautifulSoup(markdown.markdown(text), "html.parser")
    return soup.get_text(separator=" ", strip=True)


def get_canonical_base_url(request: HttpRequest) -> str:
    """Build the absolute base URL (scheme + host) for canonical/social/JSON-LD metadata.

    Prefers the explicit `CANONICAL_HOST` setting so a single missing or
    misconfigured `Host` header can't poison every metadata tag. Falls back to
    the request's own scheme/host when unset, so local development and tests
    need no configuration.
    """
    if settings.CANONICAL_HOST:
        return f"https://{settings.CANONICAL_HOST}"
    return f"{request.scheme}://{request.get_host()}"
