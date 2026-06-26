from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypedDict

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import get_language, gettext
from django.views import View

from base.models import FollowMeLink, SiteMedia
from utils.helpers import markdown_to_plaintext
from utils.types import PageMetadata

from .models import Education, Experience, PersonalInfo, ProcessStep, Project, Service

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class HomeViewContext(TypedDict):
    """Context for the HomeView."""

    page_metadata: PageMetadata
    personal_info: PersonalInfo | None
    featured_projects: list[Project]
    services: list[Service]
    process_steps: list[ProcessStep]


class MyCareerViewContext(TypedDict):
    """Context for the MyCareerView."""

    page_metadata: PageMetadata
    experiences: list[Experience]
    education_entries: list[Education]


class ProjectListViewContext(TypedDict):
    """Context for the ProjectListView."""

    page_metadata: PageMetadata
    projects: list[Project]


class ProjectDetailViewContext(TypedDict):
    """Context for the ProjectDetailView."""

    page_metadata: PageMetadata
    project: Project


class HomeView(View):
    @staticmethod
    def __get_json_ld(
        personal_info: PersonalInfo,
        request: HttpRequest,
        services: list[Service],
        social_links: list[str],
    ) -> SafeString:
        """Generate JSON-LD @graph with Person and Service schemas.

        Args:
            personal_info: The personal information instance.
            request: The HTTP request object.
            services: Active services to include as Service schema entries.
            social_links: URLs for the Person sameAs property.

        Returns:
            A SafeString containing the JSON-LD representation.
        """
        base_url = f"{request.scheme}://{request.get_host()}"
        current_lang = get_language()
        site_media = SiteMedia.get_solo()

        person: dict[str, Any] = {
            "@type": "Person",
            "name": personal_info.name,
            "jobTitle": personal_info.title,
            "description": markdown_to_plaintext(personal_info.introduction),
            "url": base_url,
            "image": f"{base_url}{site_media.portrait_display.url}",
        }

        if personal_info.location:
            person["homeLocation"] = {"@type": "Place", "name": personal_info.location}

        if personal_info.technologies.exists():
            person["knowsAbout"] = personal_info.technology_names

        if social_links:
            person["sameAs"] = social_links

        graph: list[dict[str, Any]] = [person]

        for service in services:
            graph.append(
                {
                    "@type": "Service",
                    "name": service.title,
                    "description": service.short_description,
                    "url": f"{base_url}{reverse('contact')}?service={service.slug}",
                }
            )

        schema: dict[str, Any] = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": current_lang,
            },
            "@graph": graph,
        }

        return mark_safe(json.dumps(schema, ensure_ascii=False))

    @classmethod
    def __get_page_metadata(
        cls,
        personal_info: PersonalInfo | None,
        request: HttpRequest,
        services: list[Service],
        social_links: list[str],
    ) -> PageMetadata:
        """Get page metadata for the home page.

        Args:
            personal_info: The personal information instance or None.
            request: The HTTP request object.
            services: Active services passed through to the JSON-LD generator.
            social_links: Social profile URLs passed through to the JSON-LD generator.

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
            json_ld=cls.__get_json_ld(personal_info, request, services, social_links),
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests for the home page.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse rendering the home page.
        """
        personal_info = PersonalInfo.objects.first()
        services = list(Service.objects.filter(is_active=True))
        social_links = list(FollowMeLink.objects.values_list("link", flat=True))

        return render(
            request,
            "index.html",
            HomeViewContext(
                page_metadata=self.__get_page_metadata(personal_info, request, services, social_links),
                personal_info=personal_info,
                featured_projects=list(Project.objects.filter(featured=True).prefetch_related("technologies")),
                services=services,
                process_steps=list(ProcessStep.objects.all()),
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
        name = PersonalInfo.objects.values_list("name", flat=True).first()
        suffix = f" | {name}" if name else ""
        return PageMetadata(
            page_title=gettext("My Career") + suffix,
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


class ProjectListView(View):
    @staticmethod
    def __get_json_ld(projects: list[Project], request: HttpRequest) -> SafeString:
        base_url = f"{request.scheme}://{request.get_host()}"
        current_lang = get_language()

        schema: dict[str, Any] = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": current_lang,
            },
            "@type": "ItemList",
            "name": gettext("Projects"),
            "description": gettext("Browse all my projects — problem, approach, and outcomes."),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": project.title,
                    "url": f"{base_url}{reverse('project-detail', kwargs={'slug': project.slug})}",
                }
                for i, project in enumerate(projects)
            ],
        }

        return mark_safe(json.dumps(schema, ensure_ascii=False))

    @classmethod
    def __get_page_metadata(cls, projects: list[Project], request: HttpRequest) -> PageMetadata:
        name = PersonalInfo.objects.values_list("name", flat=True).first()
        suffix = f" | {name}" if name else ""
        return PageMetadata(
            page_title=gettext("Projects") + suffix,
            page_description=gettext("Browse all my projects — problem, approach, and outcomes."),
            page_keywords=gettext("projects, software development, case studies"),
            json_ld=cls.__get_json_ld(projects, request),
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        projects = list(Project.objects.prefetch_related("technologies"))
        return render(
            request,
            "projects.html",
            ProjectListViewContext(
                page_metadata=self.__get_page_metadata(projects, request),
                projects=projects,
            ),
        )


class ProjectDetailView(View):
    @staticmethod
    def __get_json_ld(project: Project, request: HttpRequest) -> SafeString:
        base_url = f"{request.scheme}://{request.get_host()}"
        current_lang = get_language()

        schema: dict[str, Any] = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": current_lang,
            },
            "@type": "CreativeWork",
            "name": project.title,
            "description": markdown_to_plaintext(project.summary),
            "url": f"{base_url}{reverse('project-detail', kwargs={'slug': project.slug})}",
        }

        if project.technologies.exists():
            schema["keywords"] = ", ".join(tech.name for tech in project.technologies.all())

        if project.hero_image:
            schema["image"] = f"{base_url}{project.hero_image.url}"

        return mark_safe(json.dumps(schema, ensure_ascii=False))

    @classmethod
    def __get_page_metadata(cls, project: Project, request: HttpRequest) -> PageMetadata:
        name = PersonalInfo.objects.values_list("name", flat=True).first()
        suffix = f" | {name}" if name else ""
        return PageMetadata(
            page_title=f"{project.title}{suffix}",
            page_description=project.summary,
            page_keywords=", ".join(tech.name for tech in project.technologies.all()),
            json_ld=cls.__get_json_ld(project, request),
        )

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        project: Project = get_object_or_404(Project.objects.prefetch_related("technologies"), slug=slug)
        return render(
            request,
            "project-detail.html",
            ProjectDetailViewContext(
                page_metadata=self.__get_page_metadata(project, request),
                project=project,
            ),
        )
