from __future__ import annotations

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from base.models import SiteMedia
from home.tests.test_views.base_view_test import BaseHomeViewTest
from utils.test_utils.base_view_test_case import ElementText
from utils.test_utils.constants import HtmlTag, Language


class TestHomeViewBasics(TestCase):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)


class BaseTestHomeViewContent(BaseHomeViewTest):
    request_path = ""

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("index.html")
        self._assert_template_is_used("cotton/base.html")

    def test_json_ld_person_schema(self) -> None:
        """Test that home view includes valid JSON-LD Person schema."""
        data = self._get_json_ld_data()

        # Verify @context structure
        self.assertIn("@context", data, f"Expected '@context' key in the JSON-LD data, got keys: {list(data)}")
        self.assertIsInstance(
            data["@context"], dict, f"Expected '@context' to be a dict, got '{type(data['@context'])}'"
        )
        self.assertEqual(
            vocab := data["@context"]["@vocab"],
            "https://schema.org/",
            f"Expected '@context.@vocab' to be 'https://schema.org/', got '{vocab}'",
        )

        # Verify language
        self.assertEqual(
            language := data["@context"]["@language"],
            self.language,
            f"Expected '@context.@language' to be '{self.language}', got '{language}'",
        )

        # Verify @type
        self.assertEqual(type_ := data["@type"], "Person", f"Expected '@type' to be 'Person', got '{type_}'")

        # Verify specific fields from test data
        self.assertEqual(
            name := data["name"],
            test_view_constants.PERSONAL_INFO_NAME,
            f"Expected 'name' to be '{test_view_constants.PERSONAL_INFO_NAME}', got '{name}'",
        )
        self.assertEqual(
            job_title := data["jobTitle"],
            expected_job_title := test_view_constants.PERSONAL_INFO_TITLE[self.language],
            f"Expected 'jobTitle' to be '{expected_job_title}', got '{job_title}'",
        )
        self.assertEqual(
            description := data["description"],
            expected_description := test_view_constants.PERSONAL_INFO_INTRODUCTION[self.language],
            f"Expected 'description' to be '{expected_description}', got '{description}'",
        )
        self.assertEqual(
            url := data["url"], "http://testserver", f"Expected 'url' to be 'http://testserver', got '{url}'"
        )
        self.assertEqual(
            image := data["image"],
            expected_image := f"http://testserver{SiteMedia.get_solo().portrait_display.url}",
            f"Expected 'image' to be '{expected_image}', got '{image}'",
        )

        # Verify knowsAbout contains technologies in correct order
        expected_technologies = [
            test_view_constants.TECHNOLOGY_1[self.language],
            test_view_constants.TECHNOLOGY_2[self.language],
            test_view_constants.TECHNOLOGY_4[self.language],
            test_view_constants.TECHNOLOGY_3[self.language],
        ]
        self.assertEqual(
            knows_about := data["knowsAbout"],
            expected_technologies,
            f"Expected 'knowsAbout' to be '{expected_technologies}', got '{knows_about}'",
        )

    def test_meta_tags(self) -> None:
        """Test that meta tags have correct values for home page."""
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.HOME_VIEW_META_TITLE_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.HOME_VIEW_META_DESCRIPTION_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
                technologies=", ".join(
                    tech[self.language]
                    for tech in [
                        test_view_constants.TECHNOLOGY_1,
                        test_view_constants.TECHNOLOGY_2,
                        test_view_constants.TECHNOLOGY_4,
                    ]
                ),
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            ", ".join(
                (
                    *test_view_constants.COMMON_META_KEYWORDS[self.language],
                    test_view_constants.TECHNOLOGY_1[self.language].lower(),
                    test_view_constants.TECHNOLOGY_2[self.language].lower(),
                    test_view_constants.TECHNOLOGY_4[self.language].lower(),
                    test_view_constants.TECHNOLOGY_3[self.language].lower(),
                )
            ),
        )

    def test_seo_open_graph_tags(self) -> None:
        """Test that Open Graph tags have correct values."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            test_view_constants.HOME_VIEW_META_TITLE_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            test_view_constants.HOME_VIEW_META_DESCRIPTION_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
                technologies=", ".join(
                    tech[self.language]
                    for tech in [
                        test_view_constants.TECHNOLOGY_1,
                        test_view_constants.TECHNOLOGY_2,
                        test_view_constants.TECHNOLOGY_4,
                    ]
                ),
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().og_preview_image_display.url}",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:type"),
            "content",
            "profile",
        )

    def test_seo_twitter_card(self) -> None:
        """Test that Twitter card meta tags have correct values."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:card"),
            "content",
            "summary_large_image",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            test_view_constants.HOME_VIEW_META_TITLE_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            test_view_constants.HOME_VIEW_META_DESCRIPTION_TEMPLATE[self.language].format(
                name=test_view_constants.PERSONAL_INFO_NAME,
                title=test_view_constants.PERSONAL_INFO_TITLE[self.language],
                technologies=", ".join(
                    tech[self.language]
                    for tech in [
                        test_view_constants.TECHNOLOGY_1,
                        test_view_constants.TECHNOLOGY_2,
                        test_view_constants.TECHNOLOGY_4,
                    ]
                ),
            ),
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().twitter_preview_image_display.url}",
        )

    def test_personal_info(self) -> None:
        home = self._find_element_by_tag_and_id(self.response_data.soup, HtmlTag.DIV, test_view_constants.HOME_ID)

        self._assert_text_of_elements(
            home,
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.PERSONAL_INFO_INTRODUCTION_ID,
                expected_text=test_view_constants.PERSONAL_INFO_INTRODUCTION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.SPAN,
                element_id=test_view_constants.PERSONAL_INFO_NAME_ID,
                expected_text=test_view_constants.PERSONAL_INFO_NAME,
            ),
            ElementText(
                html_tag=HtmlTag.SPAN,
                element_id=test_view_constants.PERSONAL_INFO_TITLE_ID,
                expected_text=test_view_constants.PERSONAL_INFO_TITLE[self.language],
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
            self._find_element_by_tag_and_id(home, HtmlTag.DIALOG, test_view_constants.ABOUT_ME_MODAL_ID),
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

    def test_cta_block(self) -> None:
        cta_section = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.SECTION, test_view_constants.HOME_CTA_ID
        )

        self._assert_text_of_elements(
            cta_section,
            ElementText(
                html_tag=HtmlTag.SPAN,
                element_id=test_view_constants.HOME_CTA_EYEBROW_ID,
                expected_text=test_view_constants.HOME_CTA_EYEBROW[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H2,
                element_id=test_view_constants.HOME_CTA_TITLE_ID,
                expected_text=test_view_constants.HOME_CTA_TITLE[self.language],
            ),
        )

        primary_link = self._find_element_by_tag_and_id(cta_section, HtmlTag.A, test_view_constants.HOME_CTA_PRIMARY_ID)
        self._assert_text_of_element(primary_link, test_view_constants.HOME_CTA_PRIMARY_TEXT[self.language])
        self._assert_attribute_of_element(
            primary_link,
            common_constants.ATTR_HREF,
            f"/{self.language}/contact/",
        )


class TestHomeViewEnglish(BaseTestHomeViewContent):
    language = Language.ENGLISH


class TestHomeViewSpanish(BaseTestHomeViewContent):
    language = Language.SPANISH
