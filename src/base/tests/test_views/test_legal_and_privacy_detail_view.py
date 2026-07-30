from __future__ import annotations

import logging

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
from base.tests.test_views.base_view_test import BaseLegalAndPrivacyDetailViewTest
from utils.test_utils.constants import HtmlTag, Language

_LEGAL_AND_PRIVACY_DETAIL_TITLE_ID = "legal-and-privacy-detail-title"
_LEGAL_AND_PRIVACY_DETAIL_TEXT_ID = "legal-and-privacy-detail-text"


class TestLegalAndPrivacyDetailViewBasics(TestCase):
    def setUp(self) -> None:
        logger = logging.getLogger("django.request")
        self.addCleanup(logger.setLevel, logger.level)
        logger.setLevel(logging.CRITICAL)

    def test_non_existent_slug_returns_404(self) -> None:
        response = self.client.get("/en/legal/does-not-exist/")
        self.assertEqual(
            response.status_code,
            404,
            "A non-existent Legal and Privacy slug should return 404",
        )


class BaseTestLegalAndPrivacyDetailViewContent(BaseLegalAndPrivacyDetailViewTest):
    request_path = f"legal/{test_view_constants.LEGAL_SECTION_1_SLUG}/"

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("legal-and-privacy-detail.html")
        self._assert_template_is_used("cotton/base.html")

    def test_meta_tags(self) -> None:
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.LEGAL_SECTION_1[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.LEGAL_TEXT_1[self.language],
        )

    def test_content(self) -> None:
        self._assert_text_of_element_by_tag_and_id(
            self.response_data.soup,
            html_tag=HtmlTag.H1,
            element_id=_LEGAL_AND_PRIVACY_DETAIL_TITLE_ID,
            expected_text=test_view_constants.LEGAL_SECTION_1[self.language],
        )
        self._assert_text_of_element_by_tag_and_id(
            self.response_data.soup,
            html_tag=HtmlTag.DIV,
            element_id=_LEGAL_AND_PRIVACY_DETAIL_TEXT_ID,
            expected_text=test_view_constants.LEGAL_TEXT_1[self.language],
        )


class TestLegalAndPrivacyDetailViewEnglish(BaseTestLegalAndPrivacyDetailViewContent):
    language = Language.ENGLISH


class TestLegalAndPrivacyDetailViewSpanish(BaseTestLegalAndPrivacyDetailViewContent):
    language = Language.SPANISH
