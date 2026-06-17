from __future__ import annotations

from typing import ClassVar, Sequence

from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from home.models import Education, Experience, PersonalInfo, Project, Technology


@register(PersonalInfo)
class PersonalInfoAdmin(SingletonModelAdmin):
    filter_horizontal = ("technologies",)


@register(Experience)
class ExperienceAdmin(ModelAdmin[Experience]):
    filter_horizontal = ("technologies",)


@register(Project)
class ProjectAdmin(SortableAdminMixin, ModelAdmin[Project]):  # type: ignore[misc]
    prepopulated_fields: ClassVar[dict[str, Sequence[str]]] = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    list_display = ("title", "featured", "order")
    list_editable = ("featured",)


@register(Education)
class EducationAdmin(ModelAdmin[Education]):
    pass


@register(Technology)
class TechnologyAdmin(SortableAdminMixin, ModelAdmin[Technology]):  # type: ignore[misc]
    list_display = ("name", "priority")
