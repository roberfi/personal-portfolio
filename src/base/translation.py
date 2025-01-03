from modeltranslation.translator import TranslationOptions, register

from base.models import LegalAndPrivacy


@register(LegalAndPrivacy)
class LegalAndPrivacyTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "text",
    )
