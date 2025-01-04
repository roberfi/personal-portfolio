from typing import Any

from django import template

from base.models import FollowMeLink, LegalAndPrivacy

register = template.Library()


@register.simple_tag
def footer_data() -> dict[str, Any]:
    return {
        "legal_and_privacy": LegalAndPrivacy.objects.all(),
        "follow_me_links": FollowMeLink.objects.all(),
    }
