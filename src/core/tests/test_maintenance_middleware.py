"""Tests for the maintenance mode middleware."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from django.test import Client, TestCase, override_settings

from utils.test_utils.constants import HtmlTag, Language

MAINTENANCE_SECTION_ID = "maintenance"
MAINTENANCE_TITLE_ID = "maintenance-title"
MAINTENANCE_DESCRIPTION_ID = "maintenance-description"

MAINTENANCE_TITLE = {
    Language.ENGLISH: "Under maintenance",
    Language.SPANISH: "En mantenimiento",
}

MAINTENANCE_DESCRIPTION = {
    Language.ENGLISH: "The site is temporarily down for maintenance. It will be back shortly.",
    Language.SPANISH: "El sitio está temporalmente en mantenimiento. Volverá en breve.",
}


class TestMaintenanceMiddlewareDisabled(TestCase):
    """When MAINTENANCE_MODE is False, requests pass through normally."""

    @override_settings(MAINTENANCE_MODE=False)
    def test_home_returns_200_when_maintenance_off(self) -> None:
        response = Client().get("/en/")
        self.assertNotEqual(
            response.status_code,
            503,
            msg="Home page should not return 503 when maintenance mode is off",
        )

    @override_settings(MAINTENANCE_MODE=False)
    def test_admin_returns_200_when_maintenance_off(self) -> None:
        response = Client().get("/en/admin/", follow=True)
        self.assertNotEqual(
            response.status_code,
            503,
            msg="Admin should not return 503 when maintenance mode is off",
        )


@override_settings(MAINTENANCE_MODE=True)
class TestMaintenanceMiddlewareEnabled(TestCase):
    """When MAINTENANCE_MODE is True, public routes return 503 with the maintenance page."""

    def test_home_returns_503(self) -> None:
        response = Client().get("/en/")
        self.assertEqual(
            response.status_code,
            503,
            msg="Home page should return 503 when maintenance mode is on",
        )

    def test_uses_maintenance_template(self) -> None:
        response = Client().get("/en/")
        template_names = [t.name for t in response.templates if t.name]
        self.assertIn(
            "maintenance.html",
            template_names,
            msg="maintenance.html template should be used when maintenance mode is on",
        )

    def test_admin_bypasses_maintenance(self) -> None:
        response = Client().get("/en/admin/", follow=True)
        self.assertNotEqual(
            response.status_code,
            503,
            msg="Admin route should not return 503 even when maintenance mode is on",
        )

    def test_arbitrary_path_returns_503(self) -> None:
        response = Client().get("/en/contact/")
        self.assertEqual(
            response.status_code,
            503,
            msg="Any public path should return 503 when maintenance mode is on",
        )

    def test_maintenance_title_present(self) -> None:
        response = Client().get("/en/")
        soup = BeautifulSoup(response.content, "html.parser")
        title_el = soup.find(HtmlTag.H1, id=MAINTENANCE_TITLE_ID)
        if not isinstance(title_el, Tag):
            self.fail(f"Element with id '{MAINTENANCE_TITLE_ID}' not found in maintenance page")
        self.assertEqual(
            title_el.get_text(strip=True),
            MAINTENANCE_TITLE[Language.ENGLISH],
            msg="Maintenance title text is incorrect",
        )

    def test_maintenance_description_present(self) -> None:
        response = Client().get("/en/")
        soup = BeautifulSoup(response.content, "html.parser")
        desc_el = soup.find(HtmlTag.P, id=MAINTENANCE_DESCRIPTION_ID)
        if not isinstance(desc_el, Tag):
            self.fail(f"Element with id '{MAINTENANCE_DESCRIPTION_ID}' not found in maintenance page")
        self.assertEqual(
            desc_el.get_text(strip=True),
            MAINTENANCE_DESCRIPTION[Language.ENGLISH],
            msg="Maintenance description text is incorrect",
        )

    def test_no_navigation_present(self) -> None:
        response = Client().get("/en/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNone(
            soup.find(id="nav-bar"),
            msg="Navigation bar should not be present in maintenance page",
        )

    def test_spanish_url_shows_spanish_text(self) -> None:
        response = Client().get("/es/")
        soup = BeautifulSoup(response.content, "html.parser")
        title_el = soup.find(HtmlTag.H1, id=MAINTENANCE_TITLE_ID)
        if not isinstance(title_el, Tag):
            self.fail(f"Element with id '{MAINTENANCE_TITLE_ID}' not found in Spanish maintenance page")
        self.assertEqual(
            title_el.get_text(strip=True),
            MAINTENANCE_TITLE[Language.SPANISH],
            msg="Maintenance page should show Spanish text for /es/ URLs",
        )

    def test_html_lang_attribute_matches_url_language(self) -> None:
        response = Client().get("/es/")
        soup = BeautifulSoup(response.content, "html.parser")
        html_el = soup.find("html")
        if not isinstance(html_el, Tag):
            self.fail("html element not found in maintenance page")
        self.assertEqual(
            html_el.get("lang"),
            "es",
            msg="html[lang] attribute should match the URL language prefix",
        )
