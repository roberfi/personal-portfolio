from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views import View

from .models import Education, Experience, PersonalInfo

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "index.html",
            {
                "personal_info": PersonalInfo.objects.first(),
            },
        )


class MyCareerView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "my-career.html",
            {
                "experiences": sorted(
                    Experience.objects.all(),
                    key=lambda experience: experience.actual_end_date,
                    reverse=True,
                ),
                "education_entries": sorted(
                    Education.objects.all(),
                    key=lambda education: education.actual_end_date,
                    reverse=True,
                ),
            },
        )
