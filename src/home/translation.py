from modeltranslation.translator import TranslationOptions, register

from .models import Experience, PersonalInfo


@register(PersonalInfo)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = (
        "description",
        "biography",
    )


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "location",
        "description",
    )
