from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.shortcuts import render
from django.utils import translation

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest, HttpResponse


class MaintenanceModeMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if getattr(settings, "MAINTENANCE_MODE", False) and "/admin/" not in request.path:
            language = translation.get_language_from_request(request, check_path=True)
            translation.activate(language)
            request.LANGUAGE_CODE = language
            return render(request, "maintenance.html", status=503)
        return self.get_response(request)
