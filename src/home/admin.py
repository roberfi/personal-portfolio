from __future__ import annotations

from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from home.models import Experience, PersonalInfo, Technology


@register(PersonalInfo)
class PersonalInfoAdmin(SingletonModelAdmin):
    filter_horizontal = ("technologies",)


@register(Experience)
class ExperienceAdmin(ModelAdmin[Experience]):
    filter_horizontal = ("technologies",)


@register(Technology)
class TechnologyAdmin(ModelAdmin[Technology]):
    pass
