from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.views import View

from home.models import PersonalInfo
from utils.helpers import markdown_to_plaintext
from utils.types import PageMetadata

from .models import LegalAndPrivacy

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class LegalAndPrivacyDetailViewContext(TypedDict):
    """Context for the LegalAndPrivacyDetailView."""

    page_metadata: PageMetadata
    section: LegalAndPrivacy


class LegalAndPrivacyDetailView(View):
    @staticmethod
    def __get_page_metadata(section: LegalAndPrivacy) -> PageMetadata:
        name = PersonalInfo.objects.values_list("name", flat=True).first()
        suffix = f" | {name}" if name else ""

        return PageMetadata(
            page_title=f"{section.title}{suffix}",
            page_description=Truncator(markdown_to_plaintext(section.text)).chars(160),
            page_keywords="",
            json_ld=mark_safe(""),
        )

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        section: LegalAndPrivacy = get_object_or_404(LegalAndPrivacy, slug=slug)

        return render(
            request,
            "legal-and-privacy-detail.html",
            LegalAndPrivacyDetailViewContext(
                page_metadata=self.__get_page_metadata(section),
                section=section,
            ),
        )
