from __future__ import annotations

from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from base.models import FollowMeLink, GoogleAnalytics, LegalAndPrivacy


@register(LegalAndPrivacy)
class LegalAndPrivacyAdmin(ModelAdmin):
    pass


@register(FollowMeLink)
class FollowMeLinkAdmin(ModelAdmin):
    pass


@register(GoogleAnalytics)
class GoogleAnalyticsAdmin(SingletonModelAdmin):
    pass
