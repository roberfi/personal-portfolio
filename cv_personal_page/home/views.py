from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import PersonalInfo, Experience
from django.utils.translation import gettext as _


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "home_link_text": _("Home"),
            "biography_link_text": _("Biography"),
            "experience_link_text": _("Experience"),
            "personal_info": PersonalInfo.objects.first(),
            "experience": Experience.objects.all(),
        },
    )
