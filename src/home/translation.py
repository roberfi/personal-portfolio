from __future__ import annotations

from modeltranslation.translator import TranslationOptions, register

from .models import Experience, PersonalInfo


@register(PersonalInfo)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "introduction",
        "biography",
    )


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "location",
        "description",
    )
