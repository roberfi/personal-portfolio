from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.views import View

from utils.types import PageMetadata

if TYPE_CHECKING:
    from django.http import HttpRequest


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(
        request,
        "404.html",
        {
            "page_metadata": PageMetadata(
                page_title=gettext("Page not found"),
                page_description=gettext("The page you are looking for does not exist."),
                page_keywords="",
                json_ld=mark_safe("{}"),
            )
        },
        status=404,
    )


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
