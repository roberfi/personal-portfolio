from django.contrib.admin import ModelAdmin, register

from home.models import Experience, PersonalInfo


@register(PersonalInfo)
class PersonalInfoAdmin(ModelAdmin):
    pass


@register(Experience)
class ExperienceAdmin(ModelAdmin):
    pass
