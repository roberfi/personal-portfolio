from __future__ import annotations

from typing import ContextManager
from unittest.mock import patch

from django.test import TestCase

import home.tests.test_views.utils.home_view.constants as home_view_constants
import utils.test_utils.constants as common_constants
from base.models import FollowMeLink, LegalAndPrivacy
from home.models import Experience, PersonalInfo
from utils.test_utils.base_view_test_case import BaseViewTestCase, ElementText
from utils.test_utils.constants import HtmlTag, Language
from utils.test_utils.mocks import get_date_with_mocked_today


class TestHomeViewBasics(TestCase):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)


class BaseTestHomeViewContent(BaseViewTestCase):
    request_path = ""

    @classmethod
    def _mock_on_request(cls) -> ContextManager:
        return patch(
            "home.models.datetime.date",
            get_date_with_mocked_today(home_view_constants.MOCKED_TODAY),
        )

    @classmethod
    def init_db(cls) -> None:
        PersonalInfo.objects.create(
            name=home_view_constants.PERSONAL_INFO_NAME,
            title=home_view_constants.PERSONAL_INFO_TITLE[Language.ENGLISH],
            title_es=home_view_constants.PERSONAL_INFO_TITLE[Language.SPANISH],
            introduction=home_view_constants.PERSONAL_INFO_INTRODUCTION[Language.ENGLISH],
            introduction_es=home_view_constants.PERSONAL_INFO_INTRODUCTION[Language.SPANISH],
            biography=home_view_constants.PERSONAL_INFO_BIOGRAPHY[Language.ENGLISH],
            biography_es=home_view_constants.PERSONAL_INFO_BIOGRAPHY[Language.SPANISH],
        )

        Experience.objects.create(
            title=home_view_constants.EXPERIENCE_1_TITLE[Language.ENGLISH],
            title_es=home_view_constants.EXPERIENCE_1_TITLE[Language.SPANISH],
            location=home_view_constants.EXPERIENCE_1_LOCATION[Language.ENGLISH],
            location_es=home_view_constants.EXPERIENCE_1_LOCATION[Language.SPANISH],
            company=home_view_constants.EXPERIENCE_1_COMPANY,
            description=home_view_constants.EXPERIENCE_1_DESCRIPTION[Language.ENGLISH],
            description_es=home_view_constants.EXPERIENCE_1_DESCRIPTION[Language.SPANISH],
            start_date=home_view_constants.EXPERIENCE_1_START_DATE,
            end_date=home_view_constants.EXPERIENCE_1_END_DATE,
        )

        Experience.objects.create(
            title=home_view_constants.EXPERIENCE_2_TITLE[Language.ENGLISH],
            title_es=home_view_constants.EXPERIENCE_2_TITLE[Language.SPANISH],
            location=home_view_constants.EXPERIENCE_2_LOCATION[Language.ENGLISH],
            location_es=home_view_constants.EXPERIENCE_2_LOCATION[Language.SPANISH],
            company=home_view_constants.EXPERIENCE_2_COMPANY,
            description=home_view_constants.EXPERIENCE_2_DESCRIPTION[Language.ENGLISH],
            description_es=home_view_constants.EXPERIENCE_2_DESCRIPTION[Language.SPANISH],
            start_date=home_view_constants.EXPERIENCE_2_START_DATE,
        )

        LegalAndPrivacy.objects.create(
            title=home_view_constants.LEGAL_SECTION_1[Language.ENGLISH],
            title_es=home_view_constants.LEGAL_SECTION_1[Language.SPANISH],
            text=home_view_constants.LEGAL_TEXT_1[Language.ENGLISH],
            text_es=home_view_constants.LEGAL_TEXT_1[Language.SPANISH],
        )

        LegalAndPrivacy.objects.create(
            title=home_view_constants.LEGAL_SECTION_2[Language.ENGLISH],
            title_es=home_view_constants.LEGAL_SECTION_2[Language.SPANISH],
            text=home_view_constants.LEGAL_TEXT_2[Language.ENGLISH],
            text_es=home_view_constants.LEGAL_TEXT_2[Language.SPANISH],
        )

        FollowMeLink.objects.create(
            name=home_view_constants.FOLLOW_ME_LINK_NAME,
            link=home_view_constants.FOLLOW_ME_LINK,
            svg_view_box=home_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
            svg_path=home_view_constants.FOLLOW_ME_LINK_PATH,
        )

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("index.html")
        self._assert_template_is_used("cotton/base.html")

    def test_personal_info(self) -> None:
        home = self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.DIV, home_view_constants.HOME_ID)

        self._assert_text_of_elements(
            home,
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=home_view_constants.PERSONAL_INFO_NAME_ID,
                expected_text=home_view_constants.PERSONAL_INFO_NAME,
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=home_view_constants.PERSONAL_INFO_TITLE_ID,
                expected_text=home_view_constants.PERSONAL_INFO_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.PERSONAL_INFO_INTRODUCTION_ID,
                expected_text=home_view_constants.PERSONAL_INFO_INTRODUCTION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=home_view_constants.ABOUT_ME_BUTTON_ID,
                expected_text=home_view_constants.ABOUT_ME_BUTTON_TEXT[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(home, HtmlTag.BUTTON, home_view_constants.ABOUT_ME_BUTTON_ID),
            common_constants.ATTR_ONCLICK,
            f"{home_view_constants.ABOUT_ME_MODAL_ID}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                self._find_element_by_tag_and_id(home, HtmlTag.DIALOG, home_view_constants.ABOUT_ME_MODAL_ID),
                HtmlTag.DIV,
                home_view_constants.ABOUT_ME_ID,
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=home_view_constants.ABOUT_ME_TITLE_ID,
                expected_text=home_view_constants.ABOUT_ME_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.PERSONAL_INFO_BIOGRAPHY_ID,
                expected_text=home_view_constants.PERSONAL_INFO_BIOGRAPHY[self.language],
            ),
        )

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, home_view_constants.MY_CAREER_ID)

        self._assert_text_of_element(
            my_career,
            HtmlTag.H1,
            home_view_constants.MY_CAREER_TITLE_ID,
            home_view_constants.MY_CAREER_TITLE[self.language],
        )

        experiences = self._find_element_by_id(my_career, element_id=home_view_constants.EXPERIENCES_LIST_ID).find_all(
            HtmlTag.LI
        )

        self.assertEqual(
            number_of_experiences := len(experiences),
            home_view_constants.EXPECTED_NUMBER_OF_EXPERIENCES,
            f"There should be {home_view_constants.EXPECTED_NUMBER_OF_EXPERIENCES}"
            f" experiences, but there are {number_of_experiences}",
        )

        self._assert_text_of_elements(
            experiences[0],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=home_view_constants.EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_COMPANY_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_LOCATION[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                experiences[0],
                HtmlTag.BUTTON,
                home_view_constants.EXPERIENCE_MORE_BUTTON_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{home_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                experiences[0],
                HtmlTag.DIALOG,
                home_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=home_view_constants.MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=home_view_constants.MODAL_EXPERIENCE_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_COMPANY_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.EXPERIENCE_2_DESCRIPTION[self.language],
            ),
        )

        self._assert_text_of_elements(
            experiences[1],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=home_view_constants.EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_COMPANY_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_LOCATION[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                experiences[1],
                HtmlTag.BUTTON,
                home_view_constants.EXPERIENCE_MORE_BUTTON_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{home_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                experiences[1],
                HtmlTag.DIALOG,
                home_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=home_view_constants.MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=home_view_constants.MODAL_EXPERIENCE_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_COMPANY_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.EXPERIENCE_1_DESCRIPTION[self.language],
            ),
        )

    def test_legal_and_privacy(self) -> None:
        legal_and_privacy_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.FOOTER, home_view_constants.FOOTER_ID),
            HtmlTag.NAV,
            home_view_constants.LEGAL_AND_PRIVACY_ID,
        )

        self._assert_text_of_element(
            legal_and_privacy_section,
            html_tag=HtmlTag.H6,
            element_id=home_view_constants.LEGAL_AND_PRIVACY_TITLE_ID,
            expected_text=home_view_constants.LEGAL_AND_PRIVACY_TITLE[self.language],
        )

        self._assert_text_of_elements(
            legal_and_privacy_section,
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.LEGAL_SECTION_2[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                home_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{home_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                home_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{home_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=1),
                expected_text=home_view_constants.LEGAL_TEXT_1[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.LEGAL_SECTION_2[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=home_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=2),
                expected_text=home_view_constants.LEGAL_TEXT_2[self.language],
            ),
        )

    def test_follow_me_links(self) -> None:
        follow_me_links_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.FOOTER, home_view_constants.FOOTER_ID),
            HtmlTag.NAV,
            home_view_constants.FOLLOW_ME_LINKS_ID,
        )

        self._assert_text_of_element(
            follow_me_links_section,
            html_tag=HtmlTag.H6,
            element_id=home_view_constants.FOLLOW_ME_LINKS_TITLE_ID,
            expected_text=home_view_constants.FOLLOW_ME_LINKS_TITLE[self.language],
        )

        follow_me_link_container = self._find_element_by_tag_and_id(
            follow_me_links_section,
            html_tag=HtmlTag.DIV,
            element_id=home_view_constants.FOLLOW_ME_LINK_CONTAINER_ID_TEMPLATE.format(id=1),
        )
        self._assert_element_contains_class_name(follow_me_link_container, common_constants.CLASS_TOOLTIP)
        self._assert_attribute_of_element(
            follow_me_link_container,
            common_constants.ATTR_DATA_TIP,
            home_view_constants.FOLLOW_ME_LINK_NAME,
        )

        follow_me_link = self._find_element_by_tag_and_id(
            follow_me_link_container,
            html_tag=HtmlTag.A,
            element_id=home_view_constants.FOLLOW_ME_LINK_ID_TEMPLATE.format(id=1),
        )
        self._assert_attribute_of_element(
            follow_me_link,
            common_constants.ATTR_HREF,
            home_view_constants.FOLLOW_ME_LINK,
        )
        self._assert_attribute_of_element(follow_me_link, common_constants.ATTR_TARGET, "_blank")

        follow_me_link_svg = self._find_element_by_html_tag(follow_me_link, html_tag=HtmlTag.SVG)
        self._assert_attribute_of_element(
            follow_me_link_svg,
            common_constants.ATTR_VIEW_BOX,
            home_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
        )

        follow_me_link_path = self._find_element_by_html_tag(follow_me_link_svg, html_tag=HtmlTag.PATH)
        self._assert_attribute_of_element(
            follow_me_link_path,
            common_constants.ATTR_D,
            home_view_constants.FOLLOW_ME_LINK_PATH,
        )


class TestHomeViewEnglish(BaseTestHomeViewContent):
    language = Language.ENGLISH


class TestHomeViewSpanish(BaseTestHomeViewContent):
    language = Language.SPANISH
