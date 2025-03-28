from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, ClassVar, ContextManager, NamedTuple

from bs4 import BeautifulSoup, Tag
from django.test import Client, TestCase

if TYPE_CHECKING:
    from utils.test_utils.constants import HtmlTag, Language


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


class BaseViewTestCase(TestCase, ABC):
    request_path: ClassVar[str]
    language: ClassVar[Language]
    response_data: ClassVar[ResponseData]

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override this method to mock anything at the request made by the client."""
        return nullcontext()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.init_db()
        cls.client = Client()
        with cls._mock_on_request():
            cls.response_data = ResponseData.get_response(cls.client, f"/{cls.language}/{cls.request_path}")

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

    def _assert_text_of_element(self, soup: Tag, html_tag: HtmlTag, element_id: str, expected_text: str) -> None:
        self.assertEqual(
            actual_text := self._find_element_by_tag_and_id(soup, html_tag, element_id).get_text(strip=True),
            expected_text,
            msg=f"Text of element '{element_id}' is '{actual_text}'; expected text '{expected_text}'",
        )

    def _assert_text_of_elements(self, soup: Tag, *elements: ElementText) -> None:
        for element in elements:
            self._assert_text_of_element(soup, element.html_tag, element.element_id, element.expected_text)

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

    @classmethod
    @abstractmethod
    def init_db(cls) -> None: ...
