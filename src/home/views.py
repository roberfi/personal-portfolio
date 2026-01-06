from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypedDict

from django.shortcuts import render
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import get_language, gettext
from django.views import View

from utils.helpers import markdown_to_plaintext

from .models import Education, Experience, PersonalInfo

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class PageMetadata(TypedDict):
    """Metadata for a page used for SEO purposes."""

    page_title: str
    page_description: str
    page_keywords: str
    json_ld: SafeString


class HomeViewContext(TypedDict):
    """Context for the HomeView."""

    page_metadata: PageMetadata
    personal_info: PersonalInfo | None


class MyCareerViewContext(TypedDict):
    """Context for the MyCareerView."""

    page_metadata: PageMetadata
    experiences: list[Experience]
    education_entries: list[Education]


class HomeView(View):
    @staticmethod
    def __get_json_ld(personal_info: PersonalInfo, request: HttpRequest) -> SafeString:
        """Generate Person schema JSON-LD for the personal info.

        Args:
            personal_info: The personal information instance.
            request: The HTTP request object.

        Returns:
            A SafeString containing the JSON-LD representation.
        """
        base_url = f"{request.scheme}://{request.get_host()}"
        current_lang = get_language()

        schema = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": current_lang,
            },
            "@type": "Person",
            "name": personal_info.name,
            "jobTitle": personal_info.title,
            "description": markdown_to_plaintext(personal_info.introduction),
            "url": base_url,
            "image": f"{base_url}/media/background.jpg",
        }

        if personal_info.technologies.exists():
            schema["knowsAbout"] = personal_info.technology_names

        return mark_safe(json.dumps(schema, ensure_ascii=False))

    @classmethod
    def __get_page_metadata(cls, personal_info: PersonalInfo | None, request: HttpRequest) -> PageMetadata:
        """Get page metadata for the home page.

        Args:
            personal_info: The personal information instance or None.
            request: The HTTP request object.

        Returns:
            A PageMetadata dictionary containing SEO metadata.
        """
        if personal_info is None:
            return PageMetadata(
                page_title=gettext("Personal Portfolio"),
                page_description=gettext("Welcome to my personal portfolio website."),
                page_keywords="",
                json_ld=mark_safe(""),
            )

        return PageMetadata(
            page_title=personal_info.get_page_title(),
            page_description=personal_info.get_page_description(),
            page_keywords=personal_info.get_page_keywords(),
            json_ld=cls.__get_json_ld(personal_info, request),
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests for the home page.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse rendering the home page.
        """
        personal_info = PersonalInfo.objects.first()

        return render(
            request,
            "index.html",
            HomeViewContext(
                page_metadata=self.__get_page_metadata(personal_info, request),
                personal_info=personal_info,
            ),
        )


class MyCareerView(View):
    @staticmethod
    def __get_experiences_json_ld(experiences: list[Experience]) -> list[dict[str, Any]]:
        """Generate WorkExperience schema JSON-LD for a list of experiences.

        Args:
            experiences: A list of Experience instances.

        Returns:
            A list of dictionaries representing WorkExperience schema JSON-LD.
        """
        schemas = []

        for experience in experiences:
            schema: dict[str, Any] = {
                "@type": "WorkExperience",
                "name": experience.title,
                "description": markdown_to_plaintext(experience.description),
                "startDate": experience.start_date.isoformat(),
                "location": {
                    "@type": "Place",
                    "name": experience.location,
                },
            }

            if experience.institution:
                schema["employer"] = {
                    "@type": "Organization",
                    "name": experience.institution,
                }

            if experience.end_date:
                schema["endDate"] = experience.end_date.isoformat()

            if experience.technologies.exists():
                schema["skills"] = [tech.name for tech in experience.technologies.all()]

            schemas.append(schema)

        return schemas

    @staticmethod
    def __get_education_json_ld(education_entries: list[Education]) -> list[dict[str, Any]]:
        """Generate EducationalOccupationalCredential schema JSON-LD for a list of education entries.

        Args:
            education_entries: A list of Education instances.

        Returns:
            A list of dictionaries representing EducationalOccupationalCredential schema JSON-LD.
        """
        schemas = []

        for education in education_entries:
            schema: dict[str, Any] = {
                "@type": "EducationalOccupationalCredential",
                "name": education.title,
                "description": markdown_to_plaintext(education.description),
                "educationalLevel": education.title,
                "dateCreated": education.start_date.isoformat(),
                "recognizedBy": {
                    "@type": "EducationalOrganization",
                    "name": education.institution,
                    "location": {
                        "@type": "Place",
                        "name": education.location,
                    },
                },
            }

            if education.end_date:
                schema["validFrom"] = education.end_date.isoformat()

            schemas.append(schema)

        return schemas

    @classmethod
    def __get_json_ld(cls, experiences: list[Experience], education_entries: list[Education]) -> SafeString:
        """Generate MyCareer schema JSON-LD.

        Args:
            experiences: A list of Experience instances.
            education_entries: A list of Education instances.

        Returns:
            A SafeString containing the JSON-LD representation.
        """
        current_lang = get_language()

        schema: dict[str, Any] = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": current_lang,
            },
            "@graph": [
                *cls.__get_experiences_json_ld(experiences),
                *cls.__get_education_json_ld(education_entries),
            ],
        }

        return mark_safe(json.dumps(schema, ensure_ascii=False))

    @classmethod
    def __get_page_metadata(cls, experiences: list[Experience], education_entries: list[Education]) -> PageMetadata:
        """Get page metadata for the My Career page.

        Args:
            experiences: A list of Experience instances.
            education_entries: A list of Education instances.

        Returns:
            A PageMetadata dictionary containing SEO metadata.
        """
        return PageMetadata(
            page_title=gettext("My Career | Professional Experience & Education"),
            page_description=gettext(
                "Professional experience and educational background."
                " View my complete career history, work experience, and academic qualifications."
            ),
            page_keywords=gettext("experience, education, professional background, work history"),
            json_ld=cls.__get_json_ld(experiences, education_entries),
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests for the home page.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse rendering the My Career page.
        """
        experiences = sorted(
            Experience.objects.all(),
            key=lambda experience: experience.actual_end_date,
            reverse=True,
        )
        education_entries = sorted(
            Education.objects.all(),
            key=lambda education: education.actual_end_date,
            reverse=True,
        )

        return render(
            request,
            "my-career.html",
            MyCareerViewContext(
                page_metadata=self.__get_page_metadata(experiences, education_entries),
                experiences=experiences,
                education_entries=education_entries,
            ),
        )
