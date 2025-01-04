from django.contrib.admin import ModelAdmin, register

from base.models import FollowMeLink, LegalAndPrivacy


@register(LegalAndPrivacy)
class LegalAndPrivacyAdmin(ModelAdmin):
    pass


@register(FollowMeLink)
class FollowMeLinkAdmin(ModelAdmin):
    pass
