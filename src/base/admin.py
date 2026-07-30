from __future__ import annotations

from typing import ClassVar, Sequence

from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from base.models import FollowMeLink, GoogleAnalytics, LegalAndPrivacy, SiteMedia


@register(LegalAndPrivacy)
class LegalAndPrivacyAdmin(ModelAdmin[LegalAndPrivacy]):
    prepopulated_fields: ClassVar[dict[str, Sequence[str]]] = {"slug": ("title",)}


@register(FollowMeLink)
class FollowMeLinkAdmin(ModelAdmin[FollowMeLink]):
    pass


@register(GoogleAnalytics)
class GoogleAnalyticsAdmin(SingletonModelAdmin):
    pass


@register(SiteMedia)
class SiteMediaAdmin(SingletonModelAdmin):
    pass
