from __future__ import annotations

import logging

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from base.models import SiteMedia
from home.tests.test_views.base_view_test import BaseHomeViewTest
from utils.test_utils.base_view_test_case import ElementText
from utils.test_utils.constants import HtmlTag, Language


class TestProjectDetailViewBasics(TestCase):
    def setUp(self) -> None:
        logger = logging.getLogger("django.request")
        self.addCleanup(logger.setLevel, logger.level)
        logger.setLevel(logging.CRITICAL)

    def test_non_existent_slug_returns_404(self) -> None:
        response = self.client.get("/en/projects/does-not-exist/")
        self.assertEqual(
            response.status_code,
            404,
            "A non-existent project slug should return 404",
        )


class BaseTestProjectDetailViewContent(BaseHomeViewTest):
    request_path = f"projects/{test_view_constants.PROJECT_1_SLUG}/"

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("project-detail.html")
        self._assert_template_is_used("cotton/base.html")
        self._assert_template_is_used("cotton/project_detail.html")

    def test_meta_tags(self) -> None:
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.PROJECT_DETAIL_VIEW_META_TITLE_TEMPLATE[self.language].format(
                title=test_view_constants.PROJECT_1_TITLE[self.language]
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.PROJECT_1_SUMMARY[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            ", ".join(
                (
                    *test_view_constants.COMMON_META_KEYWORDS[self.language],
                    test_view_constants.TECHNOLOGY_1[self.language],
                    test_view_constants.TECHNOLOGY_2[self.language],
                )
            ),
        )

    def test_seo_open_graph_tags(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            test_view_constants.PROJECT_DETAIL_VIEW_META_TITLE_TEMPLATE[self.language].format(
                title=test_view_constants.PROJECT_1_TITLE[self.language]
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            test_view_constants.PROJECT_1_SUMMARY[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().og_preview_image_display.url}",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/",
        )

    def test_seo_twitter_card(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            test_view_constants.PROJECT_DETAIL_VIEW_META_TITLE_TEMPLATE[self.language].format(
                title=test_view_constants.PROJECT_1_TITLE[self.language]
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            test_view_constants.PROJECT_1_SUMMARY[self.language],
        )

    def test_json_ld_creative_work_schema(self) -> None:
        data = self._get_json_ld_data()

        self.assertEqual(
            data["@context"]["@vocab"],
            "https://schema.org/",
            f"Expected '@context.@vocab' to be 'https://schema.org/', got '{data['@context']['@vocab']}'",
        )
        self.assertEqual(
            data["@context"]["@language"],
            self.language,
            f"Expected '@context.@language' to be '{self.language}', got '{data['@context']['@language']}'",
        )
        self.assertEqual(
            data["@type"],
            "CreativeWork",
            f"Expected '@type' to be 'CreativeWork', got '{data['@type']}'",
        )
        self.assertEqual(
            data["name"],
            test_view_constants.PROJECT_1_TITLE[self.language],
            f"Expected 'name' to be '{test_view_constants.PROJECT_1_TITLE[self.language]}', got '{data['name']}'",
        )
        self.assertEqual(
            data["description"],
            test_view_constants.PROJECT_1_SUMMARY[self.language],
            (
                f"Expected 'description' to be '{test_view_constants.PROJECT_1_SUMMARY[self.language]}',"
                f" got '{data['description']}'"
            ),
        )
        self.assertIn(
            f"/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/",
            data["url"],
            f"Expected 'url' to contain '/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/'",
        )
        self.assertEqual(
            data["keywords"],
            f"{test_view_constants.TECHNOLOGY_1[self.language]}, {test_view_constants.TECHNOLOGY_2[self.language]}",
            "Expected 'keywords' to contain technologies",
        )

    def test_project_detail_content(self) -> None:
        detail = self._find_element_by_id(self.response_data.soup, test_view_constants.PROJECT_DETAIL_ID)

        # Back link points to the projects list
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(detail, HtmlTag.A, test_view_constants.PROJECT_DETAIL_BACK_LINK_ID),
            common_constants.ATTR_HREF,
            f"/{self.language}/projects/",
        )

        # Title
        self._assert_text_of_element_by_tag_and_id(
            detail,
            html_tag=HtmlTag.H1,
            element_id=test_view_constants.PROJECT_DETAIL_TITLE_ID,
            expected_text=test_view_constants.PROJECT_1_TITLE[self.language],
        )

        # Technology badges
        self._assert_list_of_strings(
            self._find_element_by_id(detail, test_view_constants.PROJECT_DETAIL_TECHNOLOGIES_ID),
            [
                test_view_constants.TECHNOLOGY_1[self.language],
                test_view_constants.TECHNOLOGY_2[self.language],
            ],
        )

        # Problem / Approach / Outcome sections
        self._assert_text_of_elements(
            detail,
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PROJECT_DETAIL_PROBLEM_ID,
                expected_text=test_view_constants.PROJECT_1_PROBLEM[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PROJECT_DETAIL_APPROACH_ID,
                expected_text=test_view_constants.PROJECT_1_APPROACH[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PROJECT_DETAIL_OUTCOME_ID,
                expected_text=test_view_constants.PROJECT_1_OUTCOME[self.language],
            ),
        )


class TestProjectDetailViewEnglish(BaseTestProjectDetailViewContent):
    language = Language.ENGLISH


class TestProjectDetailViewSpanish(BaseTestProjectDetailViewContent):
    language = Language.SPANISH
