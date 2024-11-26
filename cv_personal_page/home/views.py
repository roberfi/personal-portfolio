from django.core.files.storage import default_storage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Experience, PersonalInfo


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "favicon_url": default_storage.url("favicon.ico"),
            "background_url": default_storage.url("background.jpg"),
            "personal_info": PersonalInfo.objects.first(),
            "experience": Experience.objects.all().order_by("-end_date"),
        },
    )
