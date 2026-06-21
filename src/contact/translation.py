from __future__ import annotations

from modeltranslation.translator import TranslationOptions, register

from .models import ContactFormConfiguration


@register(ContactFormConfiguration)
class ContactFormConfigurationTranslationOptions(TranslationOptions):
    fields = ("intro",)
