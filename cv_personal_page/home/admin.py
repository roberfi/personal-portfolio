from home.models import PersonalInfo, Experience
from django.contrib.admin import register, ModelAdmin


@register(PersonalInfo)
class PersonalInfoAdmin(ModelAdmin):
    pass


@register(Experience)
class ExperienceAdmin(ModelAdmin):
    pass
