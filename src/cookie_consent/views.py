import json
from abc import ABC, abstractmethod

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.base import View

from cookie_consent.models import CookieGroup


class SetCookiesBaseView(View, ABC):
    @staticmethod
    def _set_cookies(request: HttpRequest, cookies: dict[str, bool]) -> HttpResponseRedirect:
        response = HttpResponseRedirect(request.POST.get("next", "/"))

        response.set_cookie(
            "cookie_consent",
            json.dumps(cookies),
            max_age=60 * 60 * 24 * 365 * 1,  # 1 year
            samesite="Lax",
        )

        return response

    @staticmethod
    def _get_optional_cookie_groups() -> QuerySet[CookieGroup]:
        return CookieGroup.objects.exclude(is_required=True)

    @abstractmethod
    def post(self, request: HttpRequest) -> HttpResponseRedirect: ...


class AcceptAllCookies(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookies(
            request,
            {cookie_group.cookie_id: True for cookie_group in self._get_optional_cookie_groups()},
        )


class SetCookiePreferences(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookies(
            request,
            {
                cookie_group.cookie_id: request.POST.get(cookie_group.cookie_id) == "on"
                for cookie_group in self._get_optional_cookie_groups()
            },
        )
