from __future__ import annotations

from typing import TYPE_CHECKING

from utils.helpers import get_canonical_base_url

if TYPE_CHECKING:
    from django.http import HttpRequest


def canonical_base_url(request: HttpRequest) -> dict[str, str]:
    """Expose the absolute canonical base URL (scheme + host) to every template."""
    return {"canonical_base_url": get_canonical_base_url(request)}
