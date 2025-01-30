from django_cooco.models import BannerConfig, CookieGroup
from modeltranslation.translator import TranslationOptions, register


@register(BannerConfig)
class BannerConfigTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "text",
    )


@register(CookieGroup)
class CookieGroupTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )
