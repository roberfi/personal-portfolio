import json
from collections.abc import Iterable

from django import template
from django.http import HttpRequest

from cookie_consent.models import BannerConfig, CookieGroup

register = template.Library()


@register.simple_tag
def get_cookie_consent_banner() -> BannerConfig:
    return BannerConfig.get_solo()


@register.simple_tag
def is_cookie_consent_set(request: HttpRequest) -> bool:
    return request.COOKIES.get("cookie_consent") is not None


@register.simple_tag
def get_cookie_groups() -> Iterable[CookieGroup]:
    return CookieGroup.objects.all()


@register.simple_tag
def is_cookie_group_accepted(request: HttpRequest, cookie_group: CookieGroup | None) -> bool:
    if cookie_group is None:
        return False

    def __is_cookie_consent_accepted() -> bool:
        return json.loads(request.COOKIES.get("cookie_consent", "{}")).get(cookie_group.cookie_id, False)

    return cookie_group.is_required or __is_cookie_consent_accepted()


@register.filter(name="any_optional_cookie_group")
def any_optional_cookie_group(cookie_groups: Iterable[CookieGroup]) -> bool:
    return any(cookie_group for cookie_group in cookie_groups if not cookie_group.is_required)
