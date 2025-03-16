from __future__ import annotations

from datetime import date
from typing import ClassVar, NamedTuple
from unittest.mock import patch

from bs4 import BeautifulSoup, Tag
from django.test import Client, TestCase

from home.models import Experience, PersonalInfo
from utils.testing_utils import get_date_with_mocked_today

# Home ids
HOME_ID = "home"
PERSONAL_INFO_NAME_ID = "personal-info-name"
PERSONAL_INFO_DESCRIPTION_ID = "personal-info-description"

# About me ids
ABOUT_ME_ID = "about-me"
ABOUT_ME_TITLE_ID = "about-me-title"
PERSONAL_INFO_BIOGRAPHY_ID = "personal-info-biography"

# My Career ids
MY_CAREER_ID = "my-career"
MY_CAREER_TITLE_ID = "my-career-title"
EXPERIENCE_ITEM_ID_PREFIX = "experience-item"
EXPERIENCE_PERIOD_ID_PREFIX = "experience-period-"
EXPERIENCE_DURATION_ID_PREFIX = "experience-duration-"
EXPERIENCE_TITLE_ID_PREFIX = "experience-title-"
EXPERIENCE_COMPANY_ID_PREFIX = "experience-company-"
EXPERIENCE_LOCATION_ID_PREFIX = "experience-location-"
EXPERIENCE_MODAL_ID_PREFIX = "experience_modal_"
MODAL_EXPERIENCE_PERIOD_ID_PREFIX = "modal-experience-period-"
MODAL_EXPERIENCE_DURATION_ID_PREFIX = "modal-experience-duration-"
MODAL_EXPERIENCE_TITLE_ID_PREFIX = "modal-experience-title-"
MODAL_EXPERIENCE_COMPANY_ID_PREFIX = "modal-experience-company-"
MODAL_EXPERIENCE_LOCATION_ID_PREFIX = "modal-experience-location-"
MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX = "modal-experience-description-"

# About me texts
ABOUT_ME_TITLE_EN = "About me"
ABOUT_ME_TITLE_ES = "Sobre mí"

# My Career texts
MY_CAREER_TITLE_EN = "My Career"
MY_CAREER_TITLE_ES = "Mi Experiencia"

# Personal Info data
PERSONAL_INFO_NAME = "Test Name"
PERSONAL_INFO_DESCRIPTION = "Test description"
PERSONAL_INFO_DESCRIPTION_ES = "Descripción de prueba"
PERSONAL_INFO_BIOGRAPHY = "Test biography"
PERSONAL_INFO_BIOGRAPHY_ES = "Biografía de prueba"

# Experiences data
EXPERIENCE_1_TITLE = "Experience 1"
EXPERIENCE_1_TITLE_ES = "Experiencia 1"
EXPERIENCE_1_LOCATION = "Test Location 1"
EXPERIENCE_1_LOCATION_ES = "Ubicación de prueba 1"
EXPERIENCE_1_COMPANY = "Test Company 1"
EXPERIENCE_1_DESCRIPTION = "Test description 1"
EXPERIENCE_1_DESCRIPTION_ES = "Descripción de prueba 1"
EXPERIENCE_1_START_DATE = date(2021, 1, 1)
EXPERIENCE_1_END_DATE = date(2022, 3, 24)
EXPERIENCE_1_PERIOD_EN = "Jan, 2021 - Mar, 2022"
EXPERIENCE_1_PERIOD_ES = "Ene, 2021 - Mar, 2022"
EXPERIENCE_1_DURATION_EN = "(1 year, 2 months)"
EXPERIENCE_1_DURATION_ES = "(1 año, 2 meses)"

EXPERIENCE_2_TITLE = "Experience 2"
EXPERIENCE_2_TITLE_ES = "Experiencia 2"
EXPERIENCE_2_LOCATION = "Test Location 2"
EXPERIENCE_2_LOCATION_ES = "Ubicación de prueba 2"
EXPERIENCE_2_COMPANY = "Test Company 2"
EXPERIENCE_2_DESCRIPTION = "Test description 2"
EXPERIENCE_2_DESCRIPTION_ES = "Descripción de prueba 2"
EXPERIENCE_2_START_DATE = date(2022, 4, 1)
EXPERIENCE_2_PERIOD_EN = "Apr, 2022 - Present"
EXPERIENCE_2_PERIOD_ES = "Abr, 2022 - Actualmente"
EXPERIENCE_2_DURATION_EN = "(2 years, 3 months)"
EXPERIENCE_2_DURATION_ES = "(2 años, 3 meses)"

EXPECTED_NUMBER_OF_EXPERIENCES = 2

# Mocked today date
MOCKED_TODAY = date(2024, 7, 15)


class ResponseData(NamedTuple):
    status_code: int
    templates: list[str]
    soup: Tag

    @classmethod
    def get_response(cls, client: Client, url: str) -> ResponseData:
        response = client.get(url, follow=True)
        return cls(
            status_code=response.status_code,
            templates=[template.name for template in response.templates if template.name],
            soup=BeautifulSoup(response.content, "html.parser"),
        )


class ElementText(NamedTuple):
    element_id: str
    expected_text: str


class BaseTestHomeView(TestCase):
    def _find_element_by_id(self, soup: Tag, element_id: str) -> Tag:
        if not isinstance(element := soup.find(id=element_id), Tag):
            self.fail(f"Element with id '{element_id}' not found")

        return element

    def _assert_text_of_element(self, soup: Tag, element_id: str, expected_text: str) -> None:
        self.assertEqual(
            actual_text := self._find_element_by_id(soup, element_id).get_text(strip=True),
            expected_text,
            msg=f"Text of element '{element_id}' is '{actual_text}'; expected text '{expected_text}'",
        )

    def _assert_text_of_elements(self, soup: Tag, *elements: ElementText) -> None:
        for element in elements:
            self._assert_text_of_element(soup, element.element_id, element.expected_text)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

        PersonalInfo.objects.create(
            name=PERSONAL_INFO_NAME,
            description=PERSONAL_INFO_DESCRIPTION,
            description_es=PERSONAL_INFO_DESCRIPTION_ES,
            biography=PERSONAL_INFO_BIOGRAPHY,
            biography_es=PERSONAL_INFO_BIOGRAPHY_ES,
        )

        Experience.objects.create(
            title=EXPERIENCE_1_TITLE,
            title_es=EXPERIENCE_1_TITLE_ES,
            location=EXPERIENCE_1_LOCATION,
            location_es=EXPERIENCE_1_LOCATION_ES,
            company=EXPERIENCE_1_COMPANY,
            description=EXPERIENCE_1_DESCRIPTION,
            description_es=EXPERIENCE_1_DESCRIPTION_ES,
            start_date=EXPERIENCE_1_START_DATE,
            end_date=EXPERIENCE_1_END_DATE,
        )

        Experience.objects.create(
            title=EXPERIENCE_2_TITLE,
            title_es=EXPERIENCE_2_TITLE_ES,
            location=EXPERIENCE_2_LOCATION,
            location_es=EXPERIENCE_2_LOCATION_ES,
            company=EXPERIENCE_2_COMPANY,
            description=EXPERIENCE_2_DESCRIPTION,
            description_es=EXPERIENCE_2_DESCRIPTION_ES,
            start_date=EXPERIENCE_2_START_DATE,
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
        with patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY)):
            cls.response_data = ResponseData.get_response(cls.client, "/en/")

    def test_response(self) -> None:
        self.assertEqual(self.response_data.status_code, 200, "The response status code is not 200")
        self.assertIn("index.html", self.response_data.templates, "The 'index.html' template is not used")

    def test_personal_info(self) -> None:
        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, HOME_ID),
            ElementText(element_id=PERSONAL_INFO_NAME_ID, expected_text=PERSONAL_INFO_NAME),
            ElementText(element_id=PERSONAL_INFO_DESCRIPTION_ID, expected_text=PERSONAL_INFO_DESCRIPTION),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, ABOUT_ME_ID),
            ElementText(element_id=ABOUT_ME_TITLE_ID, expected_text=ABOUT_ME_TITLE_EN),
            ElementText(element_id=PERSONAL_INFO_BIOGRAPHY_ID, expected_text=PERSONAL_INFO_BIOGRAPHY),
        )

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, MY_CAREER_ID)

        self._assert_text_of_element(my_career, MY_CAREER_TITLE_ID, MY_CAREER_TITLE_EN)

        experiences = my_career.find_all("li", id=lambda _id: _id and _id.startswith(EXPERIENCE_ITEM_ID_PREFIX))
        self.assertEqual(
            number_of_experiences := len(experiences),
            EXPECTED_NUMBER_OF_EXPERIENCES,
            f"There should be {EXPECTED_NUMBER_OF_EXPERIENCES} experiences, but there are {number_of_experiences}",
        )

        self._assert_text_of_elements(
            experiences[0],
            ElementText(element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}2", expected_text=EXPERIENCE_2_PERIOD_EN),
            ElementText(element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DURATION_EN),
            ElementText(element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}2", expected_text=EXPERIENCE_2_TITLE),
            ElementText(element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}2", expected_text=EXPERIENCE_2_COMPANY),
            ElementText(element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_LOCATION),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[0], f"{EXPERIENCE_MODAL_ID_PREFIX}2"),
            ElementText(element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}2", expected_text=EXPERIENCE_2_PERIOD_EN),
            ElementText(element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DURATION_EN),
            ElementText(element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}2", expected_text=EXPERIENCE_2_TITLE),
            ElementText(element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}2", expected_text=EXPERIENCE_2_COMPANY),
            ElementText(element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_LOCATION),
            ElementText(
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DESCRIPTION
            ),
        )

        self._assert_text_of_elements(
            experiences[1],
            ElementText(element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}1", expected_text=EXPERIENCE_1_PERIOD_EN),
            ElementText(element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DURATION_EN),
            ElementText(element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}1", expected_text=EXPERIENCE_1_TITLE),
            ElementText(element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}1", expected_text=EXPERIENCE_1_COMPANY),
            ElementText(element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_LOCATION),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[1], f"{EXPERIENCE_MODAL_ID_PREFIX}1"),
            ElementText(element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}1", expected_text=EXPERIENCE_1_PERIOD_EN),
            ElementText(element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DURATION_EN),
            ElementText(element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}1", expected_text=EXPERIENCE_1_TITLE),
            ElementText(element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}1", expected_text=EXPERIENCE_1_COMPANY),
            ElementText(element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_LOCATION),
            ElementText(
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DESCRIPTION
            ),
        )


class TestHomeViewSpanish(BaseTestHomeView):
    response_data: ClassVar[ResponseData]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        with patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY)):
            cls.response_data = ResponseData.get_response(cls.client, "/es/")

    def test_response(self) -> None:
        self.assertEqual(self.response_data.status_code, 200, "The response status code is not 200")
        self.assertIn("index.html", self.response_data.templates, "The 'index.html' template is not used")

    def test_personal_info(self) -> None:
        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, HOME_ID),
            ElementText(element_id=PERSONAL_INFO_NAME_ID, expected_text=PERSONAL_INFO_NAME),
            ElementText(element_id=PERSONAL_INFO_DESCRIPTION_ID, expected_text=PERSONAL_INFO_DESCRIPTION_ES),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, ABOUT_ME_ID),
            ElementText(element_id=ABOUT_ME_TITLE_ID, expected_text=ABOUT_ME_TITLE_ES),
            ElementText(element_id=PERSONAL_INFO_BIOGRAPHY_ID, expected_text=PERSONAL_INFO_BIOGRAPHY_ES),
        )

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, MY_CAREER_ID)

        self._assert_text_of_element(my_career, MY_CAREER_TITLE_ID, MY_CAREER_TITLE_ES)

        experiences = my_career.find_all("li", id=lambda _id: _id and _id.startswith(EXPERIENCE_ITEM_ID_PREFIX))
        self.assertEqual(
            number_of_experiences := len(experiences),
            EXPECTED_NUMBER_OF_EXPERIENCES,
            f"There should be {EXPECTED_NUMBER_OF_EXPERIENCES} experiences, but there are {number_of_experiences}",
        )

        self._assert_text_of_elements(
            experiences[0],
            ElementText(element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}2", expected_text=EXPERIENCE_2_PERIOD_ES),
            ElementText(element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DURATION_ES),
            ElementText(element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}2", expected_text=EXPERIENCE_2_TITLE_ES),
            ElementText(element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}2", expected_text=EXPERIENCE_2_COMPANY),
            ElementText(element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_LOCATION_ES),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[0], f"{EXPERIENCE_MODAL_ID_PREFIX}2"),
            ElementText(element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}2", expected_text=EXPERIENCE_2_PERIOD_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DURATION_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}2", expected_text=EXPERIENCE_2_TITLE_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}2", expected_text=EXPERIENCE_2_COMPANY),
            ElementText(element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}2", expected_text=EXPERIENCE_2_LOCATION_ES),
            ElementText(
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}2", expected_text=EXPERIENCE_2_DESCRIPTION_ES
            ),
        )

        self._assert_text_of_elements(
            experiences[1],
            ElementText(element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}1", expected_text=EXPERIENCE_1_PERIOD_ES),
            ElementText(element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DURATION_ES),
            ElementText(element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}1", expected_text=EXPERIENCE_1_TITLE_ES),
            ElementText(element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}1", expected_text=EXPERIENCE_1_COMPANY),
            ElementText(element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_LOCATION_ES),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[1], f"{EXPERIENCE_MODAL_ID_PREFIX}1"),
            ElementText(element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}1", expected_text=EXPERIENCE_1_PERIOD_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DURATION_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}1", expected_text=EXPERIENCE_1_TITLE_ES),
            ElementText(element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}1", expected_text=EXPERIENCE_1_COMPANY),
            ElementText(element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}1", expected_text=EXPERIENCE_1_LOCATION_ES),
            ElementText(
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}1", expected_text=EXPERIENCE_1_DESCRIPTION_ES
            ),
        )
