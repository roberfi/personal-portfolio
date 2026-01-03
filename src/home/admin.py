from __future__ import annotations

from django.contrib.admin import ModelAdmin, StackedInline, register
from solo.admin import SingletonModelAdmin

from home.models import Education, Experience, PersonalInfo, SubProject, Technology


@register(PersonalInfo)
class PersonalInfoAdmin(SingletonModelAdmin):
    filter_horizontal = ("technologies",)


class SubProjectInline(StackedInline[SubProject, Experience]):
    model = SubProject
    extra = 0
    classes = ("collapse",)
    filter_horizontal = ("technologies",)


@register(Experience)
class ExperienceAdmin(ModelAdmin[Experience]):
    filter_horizontal = ("technologies",)
    inlines = (SubProjectInline,)


@register(SubProject)
class SubProjectAdmin(ModelAdmin[SubProject]):
    filter_horizontal = ("technologies",)


@register(Education)
class EducationAdmin(ModelAdmin[Education]):
    pass


@register(Technology)
class TechnologyAdmin(ModelAdmin[Technology]):
    pass
