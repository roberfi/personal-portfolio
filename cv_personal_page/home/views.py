from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import PersonalInfo, Experience


def home_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
        {
            "personal_info": PersonalInfo.objects.first(),
            "experience": Experience.objects.all(),
        },
    )
