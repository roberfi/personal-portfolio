from modeltranslation.translator import TranslationOptions, register

from cookie_consent.models import BannerConfig, CookieGroup


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
