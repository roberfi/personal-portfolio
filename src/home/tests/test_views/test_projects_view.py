from __future__ import annotations

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from base.models import SiteMedia
from home.tests.test_views.base_view_test import BaseHomeViewTest
from utils.test_utils.base_view_test_case import ElementText
from utils.test_utils.constants import HtmlTag, Language


class TestProjectsViewBasics(TestCase):
    def test_projects_view_redirects(self) -> None:
        response = self.client.get("/projects/")
        self.assertRedirects(response, "/en/projects/", status_code=302, target_status_code=200)


class BaseTestProjectsViewContent(BaseHomeViewTest):
    request_path = "projects/"

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("projects.html")
        self._assert_template_is_used("cotton/base.html")

    def test_meta_tags(self) -> None:
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.PROJECTS_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.PROJECTS_VIEW_META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            ", ".join(
                (
                    *test_view_constants.COMMON_META_KEYWORDS[self.language],
                    *test_view_constants.PROJECTS_VIEW_META_KEYWORDS[self.language],
                )
            ),
        )

    def test_seo_open_graph_tags(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            test_view_constants.PROJECTS_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            test_view_constants.PROJECTS_VIEW_META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().og_preview_image_display.url}",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/projects/",
        )

    def test_seo_twitter_card(self) -> None:
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            test_view_constants.PROJECTS_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            test_view_constants.PROJECTS_VIEW_META_DESCRIPTION[self.language],
        )

    def test_json_ld_item_list_schema(self) -> None:
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
            "ItemList",
            f"Expected '@type' to be 'ItemList', got '{data['@type']}'",
        )

        items = data["itemListElement"]
        self.assertEqual(
            len(items),
            3,
            f"Expected 3 items in ItemList, got {len(items)}",
        )
        self.assertEqual(
            items[0]["@type"],
            "ListItem",
            f"Expected item '@type' to be 'ListItem', got '{items[0]['@type']}'",
        )
        self.assertEqual(
            items[0]["position"],
            1,
            f"Expected first item position to be 1, got '{items[0]['position']}'",
        )
        self.assertEqual(
            items[0]["name"],
            test_view_constants.PROJECT_1_TITLE[self.language],
            (
                f"Expected first item name to be '{test_view_constants.PROJECT_1_TITLE[self.language]}',"
                f" got '{items[0]['name']}'"
            ),
        )
        self.assertIn(
            f"/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/",
            items[0]["url"],
            f"Expected first item URL to contain '/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/'",
        )

    def test_projects_section(self) -> None:
        section = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.SECTION, test_view_constants.PROJECTS_SECTION_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            section,
            html_tag=HtmlTag.H1,
            element_id=test_view_constants.PROJECTS_TITLE_ID,
            expected_text=test_view_constants.PROJECTS_SECTION_TITLE[self.language],
        )

        grid = self._find_element_by_id(section, test_view_constants.PROJECTS_GRID_ID)

        # All three projects should be in the grid (including the non-featured one)
        for project_id in (1, 2, 3):
            self._find_element_by_tag_and_id(
                grid, HtmlTag.ARTICLE, test_view_constants.PROJECT_CARD_ID_TEMPLATE.format(id=project_id)
            )

        # Each card has a link to the detail page
        card_1 = self._find_element_by_tag_and_id(
            grid, HtmlTag.ARTICLE, test_view_constants.PROJECT_CARD_ID_TEMPLATE.format(id=1)
        )
        self._assert_text_of_elements(
            card_1,
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.PROJECT_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.PROJECT_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.P,
                element_id=test_view_constants.PROJECT_SUMMARY_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.PROJECT_1_SUMMARY[self.language],
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                card_1, HtmlTag.A, test_view_constants.PROJECT_DETAIL_LINK_ID_TEMPLATE.format(id=1)
            ),
            common_constants.ATTR_HREF,
            f"/{self.language}/projects/{test_view_constants.PROJECT_1_SLUG}/",
        )

        card_3 = self._find_element_by_tag_and_id(
            grid, HtmlTag.ARTICLE, test_view_constants.PROJECT_CARD_ID_TEMPLATE.format(id=3)
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                card_3, HtmlTag.A, test_view_constants.PROJECT_DETAIL_LINK_ID_TEMPLATE.format(id=3)
            ),
            common_constants.ATTR_HREF,
            f"/{self.language}/projects/{test_view_constants.PROJECT_NON_FEATURED_SLUG}/",
        )


class TestProjectsViewEnglish(BaseTestProjectsViewContent):
    language = Language.ENGLISH


class TestProjectsViewSpanish(BaseTestProjectsViewContent):
    language = Language.SPANISH
