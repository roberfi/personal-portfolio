from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter
@stringfilter
def md(value: str) -> str:
    return mark_safe(markdown(value))
