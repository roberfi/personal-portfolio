from __future__ import annotations

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from home.tests.test_views.base_view_test import BaseViewTest
from utils.test_utils.base_view_test_case import ElementText
from utils.test_utils.constants import HtmlTag, Language


class TestHomeViewBasics(TestCase):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)


class BaseTestHomeViewContent(BaseViewTest):
    request_path = ""

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("index.html")
        self._assert_template_is_used("cotton/base.html")

    def test_personal_info(self) -> None:
        home = self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.DIV, test_view_constants.HOME_ID)

        self._assert_text_of_elements(
            home,
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.PERSONAL_INFO_NAME_ID,
                expected_text=test_view_constants.PERSONAL_INFO_NAME,
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.PERSONAL_INFO_TITLE_ID,
                expected_text=test_view_constants.PERSONAL_INFO_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PERSONAL_INFO_INTRODUCTION_ID,
                expected_text=test_view_constants.PERSONAL_INFO_INTRODUCTION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=test_view_constants.ABOUT_ME_BUTTON_ID,
                expected_text=test_view_constants.ABOUT_ME_BUTTON_TEXT[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(home, test_view_constants.PERSONAL_INFO_TECHNOLOGIES_ID),
            [
                test_view_constants.TECHNOLOGY_1[self.language],
                test_view_constants.TECHNOLOGY_2[self.language],
                test_view_constants.TECHNOLOGY_4[self.language],
                test_view_constants.TECHNOLOGY_3[self.language],
            ],
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(home, HtmlTag.BUTTON, test_view_constants.ABOUT_ME_BUTTON_ID),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.ABOUT_ME_MODAL_ID}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                self._find_element_by_tag_and_id(home, HtmlTag.DIALOG, test_view_constants.ABOUT_ME_MODAL_ID),
                HtmlTag.DIV,
                test_view_constants.ABOUT_ME_ID,
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.ABOUT_ME_TITLE_ID,
                expected_text=test_view_constants.ABOUT_ME_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PERSONAL_INFO_BIOGRAPHY_ID,
                expected_text=test_view_constants.PERSONAL_INFO_BIOGRAPHY[self.language],
            ),
        )


class TestHomeViewEnglish(BaseTestHomeViewContent):
    language = Language.ENGLISH


class TestHomeViewSpanish(BaseTestHomeViewContent):
    language = Language.SPANISH
