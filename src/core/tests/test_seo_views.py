"""Tests for SEO-related views (robots.txt, sitemap.xml)."""

from __future__ import annotations

from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from django.test import TestCase, override_settings
from django.urls import URLPattern, URLResolver, get_resolver, resolve
from django.utils import translation

from home.models import PersonalInfo, Project

# URL names intentionally excluded from the sitemap.
# Add a one-line reason for each entry so reviewers know it was a conscious choice.
_EXCLUDED_FROM_SITEMAP: frozenset[str] = frozenset(
    {
        "robots_txt",  # meta: crawlers read this, not users
        "django.contrib.sitemaps.views.sitemap",  # meta: the sitemap file itself
        "set_language",  # Django i18n language switcher
        "accept_all_cookies",  # cookie-consent action (django_cooco)
        "reject_all_cookies",  # cookie-consent action (django_cooco)
        "set_cookie_preferences",  # cookie-consent action (django_cooco)
    }
)


def _collect_url_names(resolver: URLResolver) -> set[str]:
    """Recursively collect named URL patterns, skipping namespaced includes (e.g. admin)."""
    names: set[str] = set()
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            if pattern.namespace:
                continue  # skip admin and other namespaced apps
            names.update(_collect_url_names(pattern))
        elif isinstance(pattern, URLPattern) and pattern.name:
            names.add(pattern.name)
    return names


def _url_names_from_sitemap_response(content: bytes) -> set[str]:
    """Parse sitemap XML and resolve each <loc> path back to its URL name.

    LocalePrefixPattern matches based on the active language, so we activate
    the language embedded in each path (e.g. 'es' from '/es/projects/') before
    calling resolve().
    """
    root = ET.fromstring(content)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    names: set[str] = set()
    for loc in root.findall(".//ns:loc", namespace):
        if loc.text is None:
            continue
        path = urlparse(loc.text).path
        lang = path.lstrip("/").split("/")[0]
        with translation.override(lang):
            url_name = resolve(path).url_name
        if url_name is not None:
            names.add(url_name)
    return names


class TestRobotsTxt(TestCase):
    def test_robots_txt_accessible(self) -> None:
        """Test that robots.txt is accessible and returns correct content type."""
        response = self.client.get("/robots.txt")
        self.assertEqual(status_code := response.status_code, 200, f"Expected status code 200, got '{status_code}'")
        self.assertEqual(
            content_type := response["Content-Type"],
            "text/plain",
            f"Expected Content-Type 'text/plain', got '{content_type}'",
        )

    def test_robots_txt_content(self) -> None:
        """Test that robots.txt contains expected directives."""
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")

        # Check for standard directives
        self.assertIn("User-agent: *", content, f"Expected 'User-agent: *' in robots.txt content: {content}")
        self.assertIn("Allow: /", content, f"Expected 'Allow: /' in robots.txt content: {content}")

        # Check for sitemap reference
        self.assertIn(
            "Sitemap: http://testserver/sitemap.xml",
            content,
            f"Expected a sitemap reference in robots.txt content: {content}",
        )


@override_settings(ROBOTS_DISALLOW_PATHS=["/cdn-cgi/", "/private/"])
class TestRobotsTxtDisallowPaths(TestCase):
    def test_disallow_lines_are_rendered(self) -> None:
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")
        self.assertIn(
            "Disallow: /cdn-cgi/",
            content,
            f"Expected 'Disallow: /cdn-cgi/' in robots.txt content: {content}",
        )
        self.assertIn(
            "Disallow: /private/",
            content,
            f"Expected 'Disallow: /private/' in robots.txt content: {content}",
        )

    def test_disallow_lines_appear_before_sitemap(self) -> None:
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")
        disallow_pos = content.index("Disallow:")
        sitemap_pos = content.index("Sitemap:")
        self.assertLess(
            disallow_pos,
            sitemap_pos,
            msg="Disallow directives should appear before the Sitemap line",
        )


@override_settings(ROBOTS_DISALLOW_PATHS=[])
class TestRobotsTxtNoDisallowPaths(TestCase):
    def test_no_disallow_lines_when_empty(self) -> None:
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")
        self.assertNotIn(
            "Disallow:",
            content,
            f"Expected no 'Disallow:' lines when ROBOTS_DISALLOW_PATHS is empty: {content}",
        )


class TestSitemapXml(TestCase):
    project: Project

    @classmethod
    def setUpTestData(cls) -> None:
        PersonalInfo.objects.create(
            name="Test User",
            title="Test Developer",
            introduction="Test intro",
            biography="Test bio",
        )
        cls.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            summary="A test project",
            problem="Problem",
            approach="Approach",
            outcome="Outcome",
        )

    def test_sitemap_accessible(self) -> None:
        """Test that sitemap.xml is accessible."""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(status_code := response.status_code, 200, f"Expected status code 200, got '{status_code}'")
        self.assertEqual(
            content_type := response["Content-Type"],
            "application/xml",
            f"Expected Content-Type 'application/xml', got '{content_type}'",
        )

    def test_sitemap_is_valid_xml(self) -> None:
        """Test that sitemap.xml is valid XML."""
        response = self.client.get("/sitemap.xml")
        try:
            ET.fromstring(response.content)
        except ET.ParseError as e:
            self.fail(f"Sitemap is not valid XML: {e}")

    def test_all_public_urls_covered_by_sitemap(self) -> None:
        """Fail when a named URL is added without updating the sitemap or the exclusion list."""
        response = self.client.get("/sitemap.xml")
        sitemap_names = _url_names_from_sitemap_response(response.content)
        all_names = _collect_url_names(get_resolver())
        missing = all_names - sitemap_names - _EXCLUDED_FROM_SITEMAP
        self.assertFalse(
            missing,
            f"URL name(s) {sorted(missing)} are not in the sitemap or _EXCLUDED_FROM_SITEMAP. "
            "Either add them to a sitemap class in core/sitemaps.py, "
            "or add them to _EXCLUDED_FROM_SITEMAP with a reason.",
        )

    def test_sitemap_structure(self) -> None:
        """Test that sitemap has correct structure."""
        response = self.client.get("/sitemap.xml")
        root = ET.fromstring(response.content)

        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # Check for urlset root element
        self.assertEqual(
            root.tag,
            expected_tag := f"{{{namespace['ns']}}}urlset",
            f"Expected root tag '{expected_tag}', got '{root.tag}'",
        )

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
