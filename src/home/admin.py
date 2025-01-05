from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from home.models import Experience, PersonalInfo


@register(PersonalInfo)
class PersonalInfoAdmin(SingletonModelAdmin):
    pass


@register(Experience)
class ExperienceAdmin(ModelAdmin):
    pass
