"""Tests for the custom 404 error page."""

from __future__ import annotations

import logging

import utils.test_utils.constants as common_constants
from base.models import SiteMedia
from utils.test_utils import base_view_test_case
from utils.test_utils.constants import HtmlTag, Language

# ── Constants ─────────────────────────────────────────────────────────────────

REQUEST_PATH = "this-page-does-not-exist/"

NOT_FOUND_SECTION_ID = "not-found"
NOT_FOUND_TITLE_ID = "not-found-title"
NOT_FOUND_DESCRIPTION_ID = "not-found-description"

NOT_FOUND_TITLE = {
    Language.ENGLISH: "Page not found",
    Language.SPANISH: "Página no encontrada",
}

NOT_FOUND_DESCRIPTION = {
    Language.ENGLISH: "The page you are looking for does not exist or has been moved.",
    Language.SPANISH: "La página que buscas no existe o ha sido movida.",
}

META_TITLE = {
    Language.ENGLISH: "Page not found",
    Language.SPANISH: "Página no encontrada",
}

META_DESCRIPTION = {
    Language.ENGLISH: "The page you are looking for does not exist.",
    Language.SPANISH: "La página que buscas no existe.",
}

META_KEYWORDS = {
    Language.ENGLISH: "portfolio, CV, biography, career",
    Language.SPANISH: "portfolio, CV, biografía, carrera",
}

HOME_LINK_TEXT = {
    Language.ENGLISH: "Go back home",
    Language.SPANISH: "Volver al inicio",
}

HOME_HREF = {
    Language.ENGLISH: "/en/",
    Language.SPANISH: "/es/",
}


# ── Base test ─────────────────────────────────────────────────────────────────


class BaseTest404ViewContent(base_view_test_case.CommonPageTestsMixin):
    request_path = REQUEST_PATH

    def setUp(self) -> None:
        logger = logging.getLogger("django.request")
        self.addCleanup(logger.setLevel, logger.level)
        logger.setLevel(logging.CRITICAL)
        super().setUp()

    @classmethod
    def init_db(cls) -> None:
        pass

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=404)
        self._assert_template_is_used("404.html")
        self._assert_template_is_used("cotton/base.html")

    def test_meta_tags(self) -> None:
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            META_KEYWORDS[self.language],
        )

    def test_seo_open_graph_tags(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().og_preview_image_display.url}",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/{REQUEST_PATH}",
        )

    def test_seo_twitter_card(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            META_DESCRIPTION[self.language],
        )

    def test_seo_hreflang_tags(self) -> None:
        """For 404 pages, hreflang tags point to the home page in each language."""
        hreflang_tags = self.response_data.soup.find_all("link", attrs={"rel": "alternate"})
        hreflang_en = next((tag for tag in hreflang_tags if tag.get("hreflang") == "en"), None)
        hreflang_es = next((tag for tag in hreflang_tags if tag.get("hreflang") == "es"), None)
        hreflang_default = next((tag for tag in hreflang_tags if tag.get("hreflang") == "x-default"), None)

        assert hreflang_en is not None, "Hreflang tag for 'en' should exist"
        assert hreflang_es is not None, "Hreflang tag for 'es' should exist"
        assert hreflang_default is not None, "Hreflang tag for 'x-default' should exist"

        self._assert_attribute_of_element(hreflang_en, "href", "http://testserver/en/")
        self._assert_attribute_of_element(hreflang_es, "href", "http://testserver/es/")
        self._assert_attribute_of_element(hreflang_default, "href", "http://testserver/en/")

    def test_page_content(self) -> None:
        section = self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.SECTION, NOT_FOUND_SECTION_ID)
        self._assert_text_of_element_by_tag_and_id(
            section,
            html_tag=HtmlTag.H1,
            element_id=NOT_FOUND_TITLE_ID,
            expected_text=NOT_FOUND_TITLE[self.language],
        )
        self._assert_text_of_element_by_tag_and_id(
            section,
            html_tag=HtmlTag.P,
            element_id=NOT_FOUND_DESCRIPTION_ID,
            expected_text=NOT_FOUND_DESCRIPTION[self.language],
        )

    def test_home_link(self) -> None:
        section = self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.SECTION, NOT_FOUND_SECTION_ID)
        home_link = self._find_element_by_tag_and_attribute(
            section, HtmlTag.A, common_constants.ATTR_HREF, HOME_HREF[self.language]
        )
        self._assert_text_of_element(home_link, HOME_LINK_TEXT[self.language])


# ── Concrete test classes ─────────────────────────────────────────────────────


class Test404ViewEnglish(BaseTest404ViewContent):
    language = Language.ENGLISH


class Test404ViewSpanish(BaseTest404ViewContent):
    language = Language.SPANISH
