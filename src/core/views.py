from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest


class RobotsTxtView(View):
    """Serve robots.txt file dynamically."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Return robots.txt content.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse containing the robots.txt content.
        """
        lines = [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")
