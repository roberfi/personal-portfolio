from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext_lazy

from base.models import FollowMeLink, GoogleAnalytics, LegalAndPrivacy

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise, StrPromise

register = template.Library()


class LinksDict(TypedDict):
    name: StrPromise
    url: str


class NavbarDataDict(TypedDict):
    links: tuple[LinksDict, ...]


NAVBAR_DATA: NavbarDataDict = NavbarDataDict(
    links=(
        LinksDict(
            name=gettext_lazy("Home"),
            url="home",
        ),
        LinksDict(
            name=gettext_lazy("My Career"),
            url="my-career",
        ),
    )
)


@register.simple_tag
def get_navbar_data() -> NavbarDataDict:
    return NAVBAR_DATA


@register.filter
@stringfilter
def url_title(value: str) -> StrOrPromise:
    for link in NAVBAR_DATA["links"]:
        if link["url"] == value:
            return link["name"]

    return ""


@register.simple_tag
def get_footer_data() -> dict[str, Any]:
    return {
        "legal_and_privacy": LegalAndPrivacy.objects.all(),
        "follow_me_links": FollowMeLink.objects.all(),
    }


@register.simple_tag
def get_google_analytics() -> GoogleAnalytics:
    return GoogleAnalytics.get_solo()
