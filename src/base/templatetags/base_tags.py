from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.translation import gettext_lazy

from base.models import FollowMeLink, GoogleAnalytics, LegalAndPrivacy, SiteMedia

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise, StrPromise

register = template.Library()


class LinksDict(TypedDict):
    name: StrPromise
    url: str
    child_urls: tuple[str, ...]


class NavbarDataDict(TypedDict):
    links: tuple[LinksDict, ...]


NAVBAR_DATA: NavbarDataDict = NavbarDataDict(
    links=(
        LinksDict(
            name=gettext_lazy("Home"),
            url="home",
            child_urls=(),
        ),
        LinksDict(
            name=gettext_lazy("Projects"),
            url="projects",
            child_urls=("project-detail",),
        ),
        LinksDict(
            name=gettext_lazy("Contact"),
            url="contact",
            child_urls=(),
        ),
    )
)


@register.simple_tag(takes_context=True)
def current_page_url(context: dict[str, Any]) -> str:
    """Generate the URL for the current page, preserving any URL kwargs (e.g. slug).

    Needed for hreflang tags on detail views where {% url name %} alone would raise
    NoReverseMatch because the URL requires kwargs.
    """
    request = context["request"]
    if request.resolver_match is None or request.resolver_match.url_name is None:
        return reverse("home")
    return reverse(request.resolver_match.url_name, kwargs=request.resolver_match.kwargs)


@register.simple_tag
def get_navbar_data() -> NavbarDataDict:
    return NAVBAR_DATA


@register.filter
def is_active(link: LinksDict, url_name: str) -> bool:
    return url_name == link["url"] or url_name in link["child_urls"]


@register.filter
@stringfilter
def url_title(value: str) -> StrOrPromise:
    for link in NAVBAR_DATA["links"]:
        if link["url"] == value or value in link["child_urls"]:
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


@register.simple_tag
def get_site_media() -> SiteMedia:
    return SiteMedia.get_solo()
