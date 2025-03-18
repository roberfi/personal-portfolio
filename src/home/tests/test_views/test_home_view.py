from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import ClassVar, NamedTuple
from unittest.mock import patch

from bs4 import BeautifulSoup, Tag
from django.test import Client, TestCase

from base.models import LegalAndPrivacy
from home.models import Experience, PersonalInfo
from utils.testing_utils import get_date_with_mocked_today


class HtmlTag(StrEnum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    DIV = "div"
    P = "p"
    A = "a"
    UL = "ul"
    LI = "li"
    NAV = "nav"
    FOOTER = "footer"
    TIME = "time"
    DIALOG = "dialog"


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

# Footer ids
FOOTER_ID = "footer"
LEGAL_AND_PRIVACY_ID = "legal-and-privacy"
LEGAL_AND_PRIVACY_TITLE_ID = "legal-and-privacy-title"
LEGAL_AND_PRIVACY_LINK_ID_PREFIX = "legal_and_privacy-link-"
LEGAL_AND_PRIVACY_MODAL_ID_PREFIX = "legal_and_privacy_modal_"
LEGAL_AND_PRIVACY_TEXT_ID_PREFIX = "legal-and-privacy-text-"

ENGLISH = "en"
SPANISH = "es"

# About me texts
ABOUT_ME_TITLE = {
    ENGLISH: "About me",
    SPANISH: "Sobre mí",
}

# My Career texts
MY_CAREER_TITLE = {
    ENGLISH: "My Career",
    SPANISH: "Mi Experiencia",
}

# Personal Info data
PERSONAL_INFO_NAME = "Test Name"
PERSONAL_INFO_DESCRIPTION = {
    ENGLISH: "Test description",
    SPANISH: "Descripción de prueba",
}
PERSONAL_INFO_BIOGRAPHY = {
    ENGLISH: "Test biography",
    SPANISH: "Biografía de prueba",
}

# Experiences data
EXPERIENCE_1_TITLE = {
    ENGLISH: "Experience 1",
    SPANISH: "Experiencia 1",
}
EXPERIENCE_1_LOCATION = {
    ENGLISH: "Test Location 1",
    SPANISH: "Ubicación de prueba 1",
}
EXPERIENCE_1_COMPANY = "Test Company 1"
EXPERIENCE_1_DESCRIPTION = {
    ENGLISH: "Test description 1",
    SPANISH: "Descripción de prueba 1",
}
EXPERIENCE_1_START_DATE = date(2021, 1, 1)
EXPERIENCE_1_END_DATE = date(2022, 3, 24)
EXPERIENCE_1_PERIOD = {
    ENGLISH: "Jan, 2021 - Mar, 2022",
    SPANISH: "Ene, 2021 - Mar, 2022",
}
EXPERIENCE_1_DURATION = {
    ENGLISH: "(1 year, 2 months)",
    SPANISH: "(1 año, 2 meses)",
}


EXPERIENCE_2_TITLE = {
    ENGLISH: "Experience 2",
    SPANISH: "Experiencia 2",
}
EXPERIENCE_2_LOCATION = {
    ENGLISH: "Test Location 2",
    SPANISH: "Ubicación de prueba 2",
}
EXPERIENCE_2_COMPANY = "Test Company 2"
EXPERIENCE_2_DESCRIPTION = {
    ENGLISH: "Test description 2",
    SPANISH: "Descripción de prueba 2",
}
EXPERIENCE_2_START_DATE = date(2022, 4, 1)
EXPERIENCE_2_PERIOD = {
    ENGLISH: "Apr, 2022 - Present",
    SPANISH: "Abr, 2022 - Actualmente",
}
EXPERIENCE_2_DURATION = {
    ENGLISH: "(2 years, 3 months)",
    SPANISH: "(2 años, 3 meses)",
}

EXPECTED_NUMBER_OF_EXPERIENCES = 2

# Mocked today date
MOCKED_TODAY = date(2024, 7, 15)


# Footer
LEGAL_AND_PRIVACY_TITLE = {
    ENGLISH: "Legal & Privacy",
    SPANISH: "Condiciones y Privacidad",
}

LEGAL_SECTION_1 = {
    ENGLISH: "Legal Section 1",
    SPANISH: "Sección Legal 1",
}
LEGAL_TEXT_1 = {
    ENGLISH: "Legal Text 1",
    SPANISH: "Texto Legal 1",
}

LEGAL_SECTION_2 = {
    ENGLISH: "Legal Section 2",
    SPANISH: "Sección Legal 2",
}
LEGAL_TEXT_2 = {
    ENGLISH: "Legal Text 2",
    SPANISH: "Texto Legal 2",
}


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
    html_tag: HtmlTag
    element_id: str
    expected_text: str


class BaseTestHomeView(TestCase):
    def _find_element_by_id(self, soup: Tag, element_id: str) -> Tag:
        if not isinstance(element := soup.find(id=element_id), Tag):
            self.fail(f"Element with id '{element_id}' not found")

        return element

    def _find_element_by_tag_and_id(self, soup: Tag, html_tag: HtmlTag, element_id: str) -> Tag:
        if not isinstance(element := soup.find(html_tag, id=element_id), Tag):
            self.fail(f"Element with tag '{html_tag}' and id '{element_id}' not found")

        return element

    def _assert_text_of_element(self, soup: Tag, html_tag: HtmlTag, element_id: str, expected_text: str) -> None:
        self.assertEqual(
            actual_text := self._find_element_by_tag_and_id(soup, html_tag, element_id).get_text(strip=True),
            expected_text,
            msg=f"Text of element '{element_id}' is '{actual_text}'; expected text '{expected_text}'",
        )

    def _assert_text_of_elements(self, soup: Tag, *elements: ElementText) -> None:
        for element in elements:
            self._assert_text_of_element(soup, element.html_tag, element.element_id, element.expected_text)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

        PersonalInfo.objects.create(
            name=PERSONAL_INFO_NAME,
            description=PERSONAL_INFO_DESCRIPTION[ENGLISH],
            description_es=PERSONAL_INFO_DESCRIPTION[SPANISH],
            biography=PERSONAL_INFO_BIOGRAPHY[ENGLISH],
            biography_es=PERSONAL_INFO_BIOGRAPHY[SPANISH],
        )

        Experience.objects.create(
            title=EXPERIENCE_1_TITLE[ENGLISH],
            title_es=EXPERIENCE_1_TITLE[SPANISH],
            location=EXPERIENCE_1_LOCATION[ENGLISH],
            location_es=EXPERIENCE_1_LOCATION[SPANISH],
            company=EXPERIENCE_1_COMPANY,
            description=EXPERIENCE_1_DESCRIPTION[ENGLISH],
            description_es=EXPERIENCE_1_DESCRIPTION[SPANISH],
            start_date=EXPERIENCE_1_START_DATE,
            end_date=EXPERIENCE_1_END_DATE,
        )

        Experience.objects.create(
            title=EXPERIENCE_2_TITLE[ENGLISH],
            title_es=EXPERIENCE_2_TITLE[SPANISH],
            location=EXPERIENCE_2_LOCATION[ENGLISH],
            location_es=EXPERIENCE_2_LOCATION[SPANISH],
            company=EXPERIENCE_2_COMPANY,
            description=EXPERIENCE_2_DESCRIPTION[ENGLISH],
            description_es=EXPERIENCE_2_DESCRIPTION[SPANISH],
            start_date=EXPERIENCE_2_START_DATE,
        )

        LegalAndPrivacy.objects.create(
            title=LEGAL_SECTION_1[ENGLISH],
            title_es=LEGAL_SECTION_1[SPANISH],
            text=LEGAL_TEXT_1[ENGLISH],
            text_es=LEGAL_TEXT_1[SPANISH],
        )

        LegalAndPrivacy.objects.create(
            title=LEGAL_SECTION_2[ENGLISH],
            title_es=LEGAL_SECTION_2[SPANISH],
            text=LEGAL_TEXT_2[ENGLISH],
            text_es=LEGAL_TEXT_2[SPANISH],
        )


class TestHomeView(BaseTestHomeView):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)


class BaseTestHomeViewContent(BaseTestHomeView):
    response_data: ClassVar[ResponseData]
    language: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        with patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY)):
            cls.response_data = ResponseData.get_response(cls.client, f"/{cls.language}/")

    def test_response(self) -> None:
        self.assertEqual(self.response_data.status_code, 200, "The response status code is not 200")
        self.assertIn(
            "index.html",
            self.response_data.templates,
            "The 'index.html' template is not used",
        )
        self.assertIn(
            "cotton/base.html",
            self.response_data.templates,
            "The 'base.html' template is not used",
        )

    def test_personal_info(self) -> None:
        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, HOME_ID),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=PERSONAL_INFO_NAME_ID,
                expected_text=PERSONAL_INFO_NAME,
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=PERSONAL_INFO_DESCRIPTION_ID,
                expected_text=PERSONAL_INFO_DESCRIPTION[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(self.response_data.soup, ABOUT_ME_ID),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=ABOUT_ME_TITLE_ID,
                expected_text=ABOUT_ME_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.P,
                element_id=PERSONAL_INFO_BIOGRAPHY_ID,
                expected_text=PERSONAL_INFO_BIOGRAPHY[self.language],
            ),
        )

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, MY_CAREER_ID)

        self._assert_text_of_element(my_career, HtmlTag.H1, MY_CAREER_TITLE_ID, MY_CAREER_TITLE[self.language])

        experiences = my_career.find_all(HtmlTag.LI, id=lambda _id: _id and _id.startswith(EXPERIENCE_ITEM_ID_PREFIX))
        self.assertEqual(
            number_of_experiences := len(experiences),
            EXPECTED_NUMBER_OF_EXPERIENCES,
            f"There should be {EXPECTED_NUMBER_OF_EXPERIENCES} experiences, but there are {number_of_experiences}",
        )

        self._assert_text_of_elements(
            experiences[0],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_LOCATION[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[0], f"{EXPERIENCE_MODAL_ID_PREFIX}2"),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}2",
                expected_text=EXPERIENCE_2_DESCRIPTION[self.language],
            ),
        )

        self._assert_text_of_elements(
            experiences[1],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=f"{EXPERIENCE_PERIOD_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_DURATION_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_TITLE_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_COMPANY_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{EXPERIENCE_LOCATION_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_LOCATION[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_id(experiences[1], f"{EXPERIENCE_MODAL_ID_PREFIX}1"),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=f"{MODAL_EXPERIENCE_PERIOD_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_DURATION_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=f"{MODAL_EXPERIENCE_TITLE_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_COMPANY_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_LOCATION_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=f"{MODAL_EXPERIENCE_DESCRIPTION_ID_PREFIX}1",
                expected_text=EXPERIENCE_1_DESCRIPTION[self.language],
            ),
        )

    def test_legal_and_privacy(self) -> None:
        legal_and_privacy_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.FOOTER, FOOTER_ID),
            HtmlTag.NAV,
            LEGAL_AND_PRIVACY_ID,
        )

        self._assert_text_of_element(
            legal_and_privacy_section,
            html_tag=HtmlTag.H6,
            element_id=LEGAL_AND_PRIVACY_TITLE_ID,
            expected_text=LEGAL_AND_PRIVACY_TITLE[self.language],
        )

        self._assert_text_of_elements(
            legal_and_privacy_section,
            ElementText(
                html_tag=HtmlTag.A,
                element_id=f"{LEGAL_AND_PRIVACY_LINK_ID_PREFIX}1",
                expected_text=LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.A,
                element_id=f"{LEGAL_AND_PRIVACY_LINK_ID_PREFIX}2",
                expected_text=LEGAL_SECTION_2[self.language],
            ),
        )

        self._assert_text_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=f"{LEGAL_AND_PRIVACY_MODAL_ID_PREFIX}1",
            ),
            html_tag=HtmlTag.DIV,
            element_id=f"{LEGAL_AND_PRIVACY_TEXT_ID_PREFIX}1",
            expected_text=LEGAL_TEXT_1[self.language],
        )

        self._assert_text_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=f"{LEGAL_AND_PRIVACY_MODAL_ID_PREFIX}2",
            ),
            html_tag=HtmlTag.DIV,
            element_id=f"{LEGAL_AND_PRIVACY_TEXT_ID_PREFIX}2",
            expected_text=LEGAL_TEXT_2[self.language],
        )


class TestHomeViewEnglish(BaseTestHomeViewContent):
    language = ENGLISH


class TestHomeViewSpanish(BaseTestHomeViewContent):
    language = SPANISH
