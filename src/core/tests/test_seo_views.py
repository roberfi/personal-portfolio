"""Tests for SEO-related views (robots.txt, sitemap.xml)."""

from __future__ import annotations

from xml.etree import ElementTree as ET

from django.test import TestCase

from home.models import PersonalInfo


class TestRobotsTxt(TestCase):
    def test_robots_txt_accessible(self) -> None:
        """Test that robots.txt is accessible and returns correct content type."""
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")

    def test_robots_txt_content(self) -> None:
        """Test that robots.txt contains expected directives."""
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")

        # Check for standard directives
        self.assertIn("User-agent: *", content)
        self.assertIn("Allow: /", content)

        # Check for sitemap reference
        self.assertIn("Sitemap: http://testserver/sitemap.xml", content)


class TestSitemapXml(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create minimal data needed for sitemap
        PersonalInfo.objects.create(
            name="Test User",
            title="Test Developer",
            introduction="Test intro",
            biography="Test bio",
        )

    def test_sitemap_accessible(self) -> None:
        """Test that sitemap.xml is accessible."""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")

    def test_sitemap_is_valid_xml(self) -> None:
        """Test that sitemap.xml is valid XML."""
        response = self.client.get("/sitemap.xml")
        try:
            ET.fromstring(response.content)
        except ET.ParseError as e:
            self.fail(f"Sitemap is not valid XML: {e}")

    def test_sitemap_contains_expected_urls(self) -> None:
        """Test that sitemap contains all expected URLs."""
        response = self.client.get("/sitemap.xml")
        root = ET.fromstring(response.content)

        # Get namespace
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # Get all location URLs
        locations = [loc.text for loc in root.findall(".//ns:loc", namespace)]

        # Check that we have entries for both languages
        self.assertEqual(len(locations), 4, "Sitemap should contain 4 URLs")
        self.assertIn("https://testserver/en/", locations)
        self.assertIn("https://testserver/es/", locations)
        self.assertIn("https://testserver/en/my-career/", locations)
        self.assertIn("https://testserver/es/my-career/", locations)

    def test_sitemap_structure(self) -> None:
        """Test that sitemap has correct structure."""
        response = self.client.get("/sitemap.xml")
        root = ET.fromstring(response.content)

        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # Check for urlset root element
        self.assertEqual(root.tag, f"{{{namespace['ns']}}}urlset")

        # Check that each url has required elements
        for url in root.findall("ns:url", namespace):
            loc = url.find("ns:loc", namespace)
            assert loc is not None, "URL entry missing <loc> element"
            assert loc.text is not None, "<loc> element has no text"
            self.assertTrue(loc.text.startswith("https://"), "URL does not start with https://")

            changefreq = url.find("ns:changefreq", namespace)
            self.assertIsNotNone(changefreq, "URL entry missing <changefreq> element")

            priority = url.find("ns:priority", namespace)
            self.assertIsNotNone(priority, "URL entry missing <priority> element")
