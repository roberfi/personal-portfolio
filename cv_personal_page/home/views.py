from django.core.files.storage import default_storage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Experience, PersonalInfo


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "personal_info": PersonalInfo.objects.first(),
            "experience": sorted(
                Experience.objects.all(),
                key=lambda experience: experience.actual_end_date,
                reverse=True,
            ),
        },
    )


def background_view(request: HttpRequest) -> HttpResponse:
    with default_storage.open("background.jpg", "rb") as favicon:
        return HttpResponse(favicon.read(), content_type="image/jpeg")
