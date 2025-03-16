from __future__ import annotations

from datetime import date
from typing import ClassVar, NamedTuple
from unittest.mock import patch

from bs4 import BeautifulSoup
from django.test import Client, TestCase

from home.models import Experience, PersonalInfo
from utils.testing_utils import get_date_with_mocked_today


class ResponseData(NamedTuple):
    status_code: int
    templates: list[str]
    soup: BeautifulSoup

    @classmethod
    def get_response(cls, client: Client, url: str) -> ResponseData:
        response = client.get(url, follow=True)
        return cls(
            status_code=response.status_code,
            templates=[template.name for template in response.templates if template.name],
            soup=BeautifulSoup(response.content, "html.parser"),
        )


class BaseTestHomeView(TestCase):
    def _assert_text_of_element(self, soup: BeautifulSoup, element_id: str, expected_text: str) -> None:
        if (element := soup.find(id=element_id)) is None:
            self.fail(f"Element with id '{element_id}' not found")

        self.assertEqual(
            actual_text := element.get_text(strip=True),
            expected_text,
            msg=f"Text of element '{element_id}' is '{actual_text}'; expected text '{expected_text}'",
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

        PersonalInfo.objects.create(
            name="Test Name",
            description="Test description",
            description_es="Descripción de prueba",
            biography="Test biography",
            biography_es="Biografía de prueba",
        )

        Experience.objects.create(
            title="Experience 1",
            title_es="Experiencia 1",
            location="Test Location 1",
            location_es="Ubicación de prueba 1",
            company="Test Company 1",
            description="Test description 1",
            description_es="Descripción de prueba 1",
            start_date=date(2021, 1, 1),
            end_date=date(2022, 3, 24),
        )

        Experience.objects.create(
            title="Experience 2",
            title_es="Experiencia 2",
            location="Test Location 2",
            location_es="Ubicación de prueba 2",
            company="Test Company 2",
            description="Test description 2",
            description_es="Descripción de prueba 2",
            start_date=date(2022, 4, 1),
        )


class TestHomeView(BaseTestHomeView):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)


class TestHomeViewEnglish(BaseTestHomeView):
    response_data: ClassVar[ResponseData]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        with patch("home.models.datetime.date", get_date_with_mocked_today(2024, 7, 15)):
            cls.response_data = ResponseData.get_response(cls.client, "/en/")

    def test_response(self) -> None:
        self.assertEqual(self.response_data.status_code, 200)
        self.assertIn("index.html", self.response_data.templates)

    def test_personal_info(self) -> None:
        self._assert_text_of_element(self.response_data.soup, "personal-info-name", "Test Name")
        self._assert_text_of_element(self.response_data.soup, "personal-info-description", "Test description")

        self._assert_text_of_element(self.response_data.soup, "about-me-title", "About me")
        self._assert_text_of_element(self.response_data.soup, "personal-info-biography", "Test biography")

    def test_experiences(self) -> None:
        experiences = self.response_data.soup.find_all("li", id=lambda _id: _id and _id.startswith("experience-item"))
        self.assertEqual(len(experiences), 2)

        self._assert_text_of_element(experiences[0], "experience-period-2", "Apr, 2022 - Present")
        self._assert_text_of_element(experiences[0], "experience-duration-2", "(2 years, 3 months)")
        self._assert_text_of_element(experiences[0], "experience-title-2", "Experience 2")
        self._assert_text_of_element(experiences[0], "experience-company-2", "Test Company 2")
        self._assert_text_of_element(experiences[0], "experience-location-2", "Test Location 2")

        experience_2_modal = experiences[0].find(id="experience_modal_2")

        self._assert_text_of_element(experience_2_modal, "modal-experience-period-2", "Apr, 2022 - Present")
        self._assert_text_of_element(experience_2_modal, "modal-experience-duration-2", "(2 years, 3 months)")
        self._assert_text_of_element(experience_2_modal, "modal-experience-title-2", "Experience 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-company-2", "Test Company 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-location-2", "Test Location 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-description-2", "Test description 2")

        self._assert_text_of_element(experiences[1], "experience-period-1", "Jan, 2021 - Mar, 2022")
        self._assert_text_of_element(experiences[1], "experience-duration-1", "(1 year, 2 months)")
        self._assert_text_of_element(experiences[1], "experience-title-1", "Experience 1")
        self._assert_text_of_element(experiences[1], "experience-company-1", "Test Company 1")
        self._assert_text_of_element(experiences[1], "experience-location-1", "Test Location 1")

        experience_1_modal = experiences[1].find(id="experience_modal_1")

        self._assert_text_of_element(experience_1_modal, "modal-experience-period-1", "Jan, 2021 - Mar, 2022")
        self._assert_text_of_element(experience_1_modal, "modal-experience-duration-1", "(1 year, 2 months)")
        self._assert_text_of_element(experience_1_modal, "modal-experience-title-1", "Experience 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-company-1", "Test Company 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-location-1", "Test Location 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-description-1", "Test description 1")


class TestHomeViewSpanish(BaseTestHomeView):
    response_data: ClassVar[ResponseData]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        with patch("home.models.datetime.date", get_date_with_mocked_today(2024, 7, 15)):
            cls.response_data = ResponseData.get_response(cls.client, "/es/")

    def test_response(self) -> None:
        self.assertEqual(self.response_data.status_code, 200)
        self.assertIn("index.html", self.response_data.templates)

    def test_personal_info(self) -> None:
        self._assert_text_of_element(self.response_data.soup, "personal-info-name", "Test Name")
        self._assert_text_of_element(self.response_data.soup, "personal-info-description", "Descripción de prueba")

        self._assert_text_of_element(self.response_data.soup, "about-me-title", "Sobre mí")
        self._assert_text_of_element(self.response_data.soup, "personal-info-biography", "Biografía de prueba")

    def test_experiences(self) -> None:
        experiences = self.response_data.soup.find_all("li", id=lambda _id: _id and _id.startswith("experience-item"))
        self.assertEqual(len(experiences), 2)

        self._assert_text_of_element(experiences[0], "experience-period-2", "Abr, 2022 - Actualmente")
        self._assert_text_of_element(experiences[0], "experience-duration-2", "(2 años, 3 meses)")
        self._assert_text_of_element(experiences[0], "experience-title-2", "Experiencia 2")
        self._assert_text_of_element(experiences[0], "experience-company-2", "Test Company 2")
        self._assert_text_of_element(experiences[0], "experience-location-2", "Ubicación de prueba 2")

        experience_2_modal = experiences[0].find(id="experience_modal_2")

        self._assert_text_of_element(experience_2_modal, "modal-experience-period-2", "Abr, 2022 - Actualmente")
        self._assert_text_of_element(experience_2_modal, "modal-experience-duration-2", "(2 años, 3 meses)")
        self._assert_text_of_element(experience_2_modal, "modal-experience-title-2", "Experiencia 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-company-2", "Test Company 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-location-2", "Ubicación de prueba 2")
        self._assert_text_of_element(experience_2_modal, "modal-experience-description-2", "Descripción de prueba 2")

        self._assert_text_of_element(experiences[1], "experience-period-1", "Ene, 2021 - Mar, 2022")
        self._assert_text_of_element(experiences[1], "experience-duration-1", "(1 año, 2 meses)")
        self._assert_text_of_element(experiences[1], "experience-title-1", "Experiencia 1")
        self._assert_text_of_element(experiences[1], "experience-company-1", "Test Company 1")
        self._assert_text_of_element(experiences[1], "experience-location-1", "Ubicación de prueba 1")

        experience_1_modal = experiences[1].find(id="experience_modal_1")

        self._assert_text_of_element(experience_1_modal, "modal-experience-period-1", "Ene, 2021 - Mar, 2022")
        self._assert_text_of_element(experience_1_modal, "modal-experience-duration-1", "(1 año, 2 meses)")
        self._assert_text_of_element(experience_1_modal, "modal-experience-title-1", "Experiencia 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-company-1", "Test Company 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-location-1", "Ubicación de prueba 1")
        self._assert_text_of_element(experience_1_modal, "modal-experience-description-1", "Descripción de prueba 1")
