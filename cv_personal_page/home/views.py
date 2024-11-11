from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import PersonalInfo, Experience


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "home_link_text": "Home",  # TODO: translations
            "biography_link_text": "Biography",  # TODO: translations
            "experience_link_text": "Experience",  # TODO: translations
            "personal_info": PersonalInfo.objects.first(),
            "experience": Experience.objects.all(),
        },
    )
