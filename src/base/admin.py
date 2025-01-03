from django.contrib.admin import ModelAdmin, register

from base.models import LegalAndPrivacy


@register(LegalAndPrivacy)
class LegalAndPrivacyAdmin(ModelAdmin):
    pass
