from __future__ import annotations

import json
from abc import ABC, abstractmethod
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, ClassVar, ContextManager, NamedTuple

from bs4 import BeautifulSoup, Tag
from django.test import Client, TestCase
from django.utils import translation

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from base.models import FollowMeLink, LegalAndPrivacy
from utils.test_utils.constants import HtmlTag, Language

if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


def get_beautiful_soup_from_response(response: _MonkeyPatchedWSGIResponse) -> Tag:
    return BeautifulSoup(response.content, "html.parser")


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
            soup=get_beautiful_soup_from_response(response),
        )


class ElementText(NamedTuple):
    html_tag: HtmlTag
    element_id: str
    expected_text: str


class BaseViewTestCase(TestCase, ABC):
    request_path: ClassVar[str]
    language: ClassVar[Language]
    response_data: ClassVar[ResponseData]

    @classmethod
    @abstractmethod
    def init_db(cls) -> None:
        """Initialize database objects specific to each test case."""

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override this method to mock anything at the request made by the client."""
        return nullcontext()

    @classmethod
    def setUpTestData(cls) -> None:
        # Ensure we're in the default language when creating database objects
        # to avoid django-modeltranslation storing values in the wrong fields
        translation.activate("en")
        cls._init_common_db()
        cls.init_db()
        cls.client = Client()
        with cls._mock_on_request():
            cls.response_data = ResponseData.get_response(cls.client, f"/{cls.language}/{cls.request_path}")

    def _get_json_ld_data(self) -> dict[str, Any]:
        script = self._find_element_by_tag_and_attribute(
            self.response_data.soup, HtmlTag.SCRIPT, "type", "application/ld+json"
        )

        assert isinstance(script.string, str), "JSON-LD script content should be a string"
        data = json.loads(script.string.strip())

        assert isinstance(data, dict), "JSON-LD data should be a dictionary"
        return data

    def _assert_reponse_status_code(self, *, expected_status_code: int) -> None:
        self.assertEqual(
            actual_status_code := self.response_data.status_code,
            expected_status_code,
            f"Response status code is '{actual_status_code}' instead of the expected '{expected_status_code}'",
        )

    def _assert_template_is_used(self, template_name: str) -> None:
        self.assertIn(template_name, self.response_data.templates, f"The '{template_name}' template is not used")

    def _find_element_by_id(self, soup: Tag, element_id: str) -> Tag:
        if not isinstance(element := soup.find(id=element_id), Tag):
            self.fail(f"Element with id '{element_id}' not found")

        return element

    def _find_element_by_html_tag(self, soup: Tag, html_tag: HtmlTag) -> Tag:
        if not isinstance(element := soup.find(html_tag), Tag):
            self.fail(f"Element with tag '{html_tag}' not found")

        return element

    def _find_element_by_tag_and_id(self, soup: Tag, html_tag: HtmlTag, element_id: str) -> Tag:
        if not isinstance(element := soup.find(html_tag, id=element_id), Tag):
            self.fail(f"Element with tag '{html_tag}' and id '{element_id}' not found")

        return element

    def _find_element_by_tag_and_attribute(self, soup: Tag, html_tag: HtmlTag, attribute: str, value: str) -> Tag:
        if not isinstance(element := soup.find(html_tag, attrs={attribute: value}), Tag):
            self.fail(f"Element with tag '{html_tag}' and {attribute}='{value}' not found")

        return element

    def _assert_text_of_element(self, element: Tag, expected_text: str) -> None:
        self.assertEqual(
            actual_text := element.get_text(strip=True, separator=" "),
            expected_text,
            msg=f"Text of element is '{actual_text}'; expected text '{expected_text}'",
        )

    def _assert_text_of_element_by_tag_and_id(
        self, soup: Tag, html_tag: HtmlTag, element_id: str, expected_text: str
    ) -> None:
        self._assert_text_of_element(self._find_element_by_tag_and_id(soup, html_tag, element_id), expected_text)

    def _assert_text_of_elements(self, soup: Tag, *elements: ElementText) -> None:
        for element in elements:
            self._assert_text_of_element_by_tag_and_id(
                soup, element.html_tag, element.element_id, element.expected_text
            )

    def _assert_element_not_exists(self, soup: Tag, element_id: str) -> None:
        element = soup.find(id=element_id)
        self.assertIsNone(
            element,
            msg=f"Element with id '{element_id}' was found but it should not exist",
        )

    def _assert_element_contains_class_name(self, element: Tag, expected_class_name: str) -> None:
        self.assertIn(
            expected_class_name,
            element["class"],
            (
                f"Element '<{element.name}>'"
                f"{f" with id '{element['id']}'" if 'id' in element.attrs else ''} "
                f"does not contain class name '{expected_class_name}'; "
                f"actual class list = '{element['class']}'"
            ),
        )

    def _assert_attribute_of_element(self, element: Tag, attribute: str, expected_content: str) -> None:
        self.assertEqual(
            element[attribute],
            expected_content,
            (
                f"Attribute of element '<{element.name}>'"
                f"{f" with id '{element['id']}'" if 'id' in element.attrs else ''} "
                f"is not equal to '{expected_content}'; actual value = '{element[attribute]}'"
            ),
        )

    def _assert_list_of_strings(self, element: Tag, expected_list: list[str]) -> None:
        self.assertListEqual(
            actual_list := list(element.stripped_strings),
            expected_list,
            msg=f"List of strings is {actual_list}; expected {expected_list}",
        )

    @classmethod
    def _init_common_db(cls) -> None:
        LegalAndPrivacy.objects.create(
            title=test_view_constants.LEGAL_SECTION_1[Language.ENGLISH],
            title_es=test_view_constants.LEGAL_SECTION_1[Language.SPANISH],
            text=test_view_constants.LEGAL_TEXT_1[Language.ENGLISH],
            text_es=test_view_constants.LEGAL_TEXT_1[Language.SPANISH],
        )

        LegalAndPrivacy.objects.create(
            title=test_view_constants.LEGAL_SECTION_2[Language.ENGLISH],
            title_es=test_view_constants.LEGAL_SECTION_2[Language.SPANISH],
            text=test_view_constants.LEGAL_TEXT_2[Language.ENGLISH],
            text_es=test_view_constants.LEGAL_TEXT_2[Language.SPANISH],
        )

        FollowMeLink.objects.create(
            name=test_view_constants.FOLLOW_ME_LINK_NAME,
            link=test_view_constants.FOLLOW_ME_LINK,
            svg_view_box=test_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
            svg_path=test_view_constants.FOLLOW_ME_LINK_PATH,
        )

    def test_legal_and_privacy(self) -> None:
        legal_and_privacy_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(
                self.response_data.soup, HtmlTag.FOOTER, test_view_constants.UPPER_FOOTER_ID
            ),
            HtmlTag.NAV,
            test_view_constants.LEGAL_AND_PRIVACY_ID,
        )

        self._assert_text_of_element_by_tag_and_id(
            legal_and_privacy_section,
            html_tag=HtmlTag.H6,
            element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID,
            expected_text=test_view_constants.LEGAL_AND_PRIVACY_TITLE[self.language],
        )

        self._assert_text_of_elements(
            legal_and_privacy_section,
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_SECTION_2[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_TEXT_1[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_SECTION_2[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_TEXT_2[self.language],
            ),
        )

    def test_follow_me_links(self) -> None:
        follow_me_links_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(
                self.response_data.soup, HtmlTag.FOOTER, test_view_constants.UPPER_FOOTER_ID
            ),
            HtmlTag.NAV,
            test_view_constants.FOLLOW_ME_LINKS_ID,
        )

        self._assert_text_of_element_by_tag_and_id(
            follow_me_links_section,
            html_tag=HtmlTag.H6,
            element_id=test_view_constants.FOLLOW_ME_LINKS_TITLE_ID,
            expected_text=test_view_constants.FOLLOW_ME_LINKS_TITLE[self.language],
        )

        follow_me_link_container = self._find_element_by_tag_and_id(
            follow_me_links_section,
            html_tag=HtmlTag.DIV,
            element_id=test_view_constants.FOLLOW_ME_LINK_CONTAINER_ID_TEMPLATE.format(id=1),
        )
        self._assert_element_contains_class_name(follow_me_link_container, common_constants.CLASS_TOOLTIP)
        self._assert_attribute_of_element(
            follow_me_link_container,
            common_constants.ATTR_DATA_TIP,
            test_view_constants.FOLLOW_ME_LINK_NAME,
        )

        follow_me_link = self._find_element_by_tag_and_id(
            follow_me_link_container,
            html_tag=HtmlTag.A,
            element_id=test_view_constants.FOLLOW_ME_LINK_ID_TEMPLATE.format(id=1),
        )
        self._assert_attribute_of_element(
            follow_me_link,
            common_constants.ATTR_HREF,
            test_view_constants.FOLLOW_ME_LINK,
        )
        self._assert_attribute_of_element(follow_me_link, common_constants.ATTR_TARGET, "_blank")

        follow_me_link_svg = self._find_element_by_html_tag(follow_me_link, html_tag=HtmlTag.SVG)
        self._assert_attribute_of_element(
            follow_me_link_svg,
            common_constants.ATTR_VIEW_BOX,
            test_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
        )

        follow_me_link_path = self._find_element_by_html_tag(follow_me_link_svg, html_tag=HtmlTag.PATH)
        self._assert_attribute_of_element(
            follow_me_link_path,
            common_constants.ATTR_D,
            test_view_constants.FOLLOW_ME_LINK_PATH,
        )

    def test_source_code_note(self) -> None:
        bottom_footer = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.FOOTER, test_view_constants.BOTTOM_FOOTER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            bottom_footer,
            html_tag=HtmlTag.ASIDE,
            element_id=test_view_constants.SOURCE_CODE_NOTE_ID,
            expected_text=test_view_constants.SOURCE_CODE_NOTE_TEXT[self.language],
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                bottom_footer,
                HtmlTag.A,
                test_view_constants.GITHUB_REPO_LINK_ID,
            ),
            common_constants.ATTR_HREF,
            test_view_constants.SOURCE_CODE_GITHUB_LINK,
        )

    def test_seo_canonical_url(self) -> None:
        """Test that canonical URL points to the correct page."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.LINK, "rel", "canonical"),
            "href",
            f"http://testserver/{self.language}/{self.request_path}",
        )

    def test_seo_hreflang_tags(self) -> None:
        """Test that hreflang tags are correct for home page."""
        hreflang_tags = self.response_data.soup.find_all("link", attrs={"rel": "alternate"})

        hreflang_en = next((tag for tag in hreflang_tags if tag.get("hreflang") == "en"), None)
        hreflang_es = next((tag for tag in hreflang_tags if tag.get("hreflang") == "es"), None)
        hreflang_default = next((tag for tag in hreflang_tags if tag.get("hreflang") == "x-default"), None)

        assert hreflang_en is not None, "Hreflang tag for 'en' should exist"
        assert hreflang_es is not None, "Hreflang tag for 'es' should exist"
        assert hreflang_default is not None, "Hreflang tag for 'x-default' should exist"

        self._assert_attribute_of_element(hreflang_en, "href", f"http://testserver/en/{self.request_path}")
        self._assert_attribute_of_element(hreflang_es, "href", f"http://testserver/es/{self.request_path}")
        self._assert_attribute_of_element(hreflang_default, "href", f"http://testserver/en/{self.request_path}")
