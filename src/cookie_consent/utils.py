import json
from collections.abc import Sequence
from typing import Any, NamedTuple, Self

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse

from cookie_consent.models import CookieGroup


class CookieConsentStatus(NamedTuple):
    version: int
    is_accepted: bool


class CookieConsent(NamedTuple):
    cookie_id: str
    current_version: int
    cookie_consent_status: CookieConsentStatus

    @property
    def is_version_outdated(self) -> bool:
        return self.current_version != self.cookie_consent_status.version

    @property
    def is_accepted(self) -> bool:
        return not self.is_version_outdated and self.cookie_consent_status.is_accepted


class CookieConsentManager:
    COOKIE_CONSENT_COOKIE_NAME = "cookie_consent"
    ONE_YEAR_IN_SECONDS = 60 * 60 * 24 * 365 * 1
    DEFAULT_COOKIE_CONSENT_STATUS = CookieConsentStatus(0, False)

    def __init__(self, *cookie_consent: CookieConsent) -> None:
        self.cookie_consents = cookie_consent

    def __getitem__(self, cookie_id: str) -> CookieConsent:
        for cookie_consent in self.cookie_consents:
            if cookie_consent.cookie_id == cookie_id:
                return cookie_consent

        message = f"Cookie ID '{cookie_id}' not found"
        raise KeyError(message)

    @staticmethod
    def __get_optional_cookie_groups() -> QuerySet[CookieGroup]:
        return CookieGroup.objects.exclude(is_required=True)

    @classmethod
    def from_request(cls, request: HttpRequest) -> Self:
        try:
            cookie_consent_dict = json.loads(request.COOKIES.get(cls.COOKIE_CONSENT_COOKIE_NAME, "{}"))
        except json.decoder.JSONDecodeError:
            cookie_consent_dict = {}

        _cookie_consents = []

        for cookie_group in cls.__get_optional_cookie_groups():
            cookie_consent_status = cookie_consent_dict.get(cookie_group.cookie_id)

            if (
                not isinstance(cookie_consent_status, Sequence)
                or len(cookie_consent_status) != len(cls.DEFAULT_COOKIE_CONSENT_STATUS)
                or not isinstance(cookie_consent_status[0], int)
                or not isinstance(cookie_consent_status[1], bool)
            ):
                cookie_consent_status = cls.DEFAULT_COOKIE_CONSENT_STATUS

            _cookie_consents.append(
                CookieConsent(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cookie_consent_status=CookieConsentStatus(*cookie_consent_status),
                )
            )

        return cls(*_cookie_consents)

    @classmethod
    def parse_cookie_consent_form(cls, cookie_consent_form: dict[str, Any]) -> Self:
        return cls(
            *(
                CookieConsent(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cookie_consent_status=CookieConsentStatus(
                        cookie_group.version, cookie_consent_form.get(cookie_group.cookie_id) == "on"
                    ),
                )
                for cookie_group in cls.__get_optional_cookie_groups()
            )
        )

    @classmethod
    def all_cookies_accepted(cls) -> Self:
        return cls(
            *(
                CookieConsent(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cookie_consent_status=CookieConsentStatus(cookie_group.version, True),
                )
                for cookie_group in cls.__get_optional_cookie_groups()
            )
        )

    def set_cookie_consent_cookie[THttpResponse: HttpResponse](self, response: THttpResponse) -> THttpResponse:
        response.set_cookie(
            self.COOKIE_CONSENT_COOKIE_NAME,
            json.dumps(
                {
                    cookie_consent.cookie_id: cookie_consent.cookie_consent_status
                    for cookie_consent in self.cookie_consents
                }
            ),
            max_age=self.ONE_YEAR_IN_SECONDS,
            samesite="Lax",
        )

        return response

    def is_any_cookie_consent_outdated(self) -> bool:
        return any(cookie_consent.is_version_outdated for cookie_consent in self.cookie_consents)

    def is_cookie_group_accepted(self, cookie_id: str) -> bool:
        return self[cookie_id].is_accepted
