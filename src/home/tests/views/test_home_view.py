from __future__ import annotations

from bs4 import BeautifulSoup
from django.test import Client, TestCase

from home.models import PersonalInfo


class HomeViewTest(TestCase):
    def __assert_text_of_element(self, soup: BeautifulSoup, element_id: str, expected_text: str) -> None:
        if (element := soup.find(id=element_id)) is None:
            self.fail(f"Element with id '{element_id}' not found")

        self.assertEqual(
            actual_text := element.get_text(strip=True),
            expected_text,
            msg=f"Text of element '{element_id}' is '{actual_text}'; expected text '{expected_text}'",
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

        PersonalInfo.objects.create(
            name="Test Name",
            description="Test description",
            description_es="Descripción de prueba",
            biography="Test biography",
            biography_es="Biografía de prueba",
        )

    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)

    def test_home_view_contents_en(self) -> None:
        response = self.client.get("/en/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        soup = BeautifulSoup(response.content, "html.parser")

        self.__assert_text_of_element(soup, "personal-info-name", "Test Name")
        self.__assert_text_of_element(soup, "personal-info-description", "Test description")

        self.__assert_text_of_element(soup, "about-me-title", "About me")
        self.__assert_text_of_element(soup, "personal-info-biography", "Test biography")

    def test_home_view_contents_es(self) -> None:
        response = self.client.get("/es/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        soup = BeautifulSoup(response.content, "html.parser")

        self.__assert_text_of_element(soup, "personal-info-name", "Test Name")
        self.__assert_text_of_element(soup, "personal-info-description", "Descripción de prueba")

        self.__assert_text_of_element(soup, "about-me-title", "Sobre mí")
        self.__assert_text_of_element(soup, "personal-info-biography", "Biografía de prueba")
