from modeltranslation.translator import register, TranslationOptions
from .models import PersonalInfo, Experience


@register(PersonalInfo)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = ("biography",)


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "location",
        "description",
    )
