from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext

from .models import Experience, PersonalInfo


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "sections": (
                (gettext("Home"), "home"),
                (gettext("About me"), "about-me"),
                (gettext("My Career"), "my-career"),
            ),
            "personal_info": PersonalInfo.objects.first(),
            "experiences": sorted(
                Experience.objects.all(),
                key=lambda experience: experience.actual_end_date,
                reverse=True,
            ),
        },
    )
