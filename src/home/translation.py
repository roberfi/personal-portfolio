from __future__ import annotations

from modeltranslation.translator import TranslationOptions, register

from .models import Education, Experience, PersonalInfo, Project, Technology


@register(Technology)
class TechnologyTranslationOptions(TranslationOptions):
    fields = ("name",)


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


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "problem",
        "approach",
        "outcome",
    )


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "institution",
        "location",
        "description",
    )
