"""Tests for the CANONICAL_HOST setting powering canonical, hreflang, OG and Twitter tags."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from django.test import TestCase, override_settings


def _find_attr(soup: Tag, tag_name: str, attrs: dict[str, str], attribute: str) -> str:
    element = soup.find(tag_name, attrs=attrs)
    assert isinstance(element, Tag), f"Element '<{tag_name}>' with attrs {attrs} not found"
    value = element[attribute]
    assert isinstance(value, str), f"Attribute '{attribute}' of '<{tag_name}>' is not a single string value"
    return value


@override_settings(CANONICAL_HOST="www.example.com")
class TestCanonicalHostSetting(TestCase):
    def test_canonical_and_social_tags_use_canonical_host(self) -> None:
        """Test that canonical, hreflang, OG and Twitter tags all use CANONICAL_HOST."""
        response = self.client.get("/en/")
        soup = BeautifulSoup(response.content, "html.parser")

        self.assertEqual(_find_attr(soup, "link", {"rel": "canonical"}, "href"), "https://www.example.com/en/")

        self.assertEqual(
            _find_attr(soup, "link", {"rel": "alternate", "hreflang": "en"}, "href"),
            "https://www.example.com/en/",
        )
        self.assertEqual(
            _find_attr(soup, "link", {"rel": "alternate", "hreflang": "x-default"}, "href"),
            "https://www.example.com/en/",
        )

        self.assertEqual(_find_attr(soup, "meta", {"property": "og:url"}, "content"), "https://www.example.com/en/")

        og_image = _find_attr(soup, "meta", {"property": "og:image"}, "content")
        self.assertTrue(
            og_image.startswith("https://www.example.com/"),
            f"Expected og:image to start with the canonical host, got '{og_image}'",
        )

        twitter_image = _find_attr(soup, "meta", {"name": "twitter:image"}, "content")
        self.assertTrue(
            twitter_image.startswith("https://www.example.com/"),
            f"Expected twitter:image to start with the canonical host, got '{twitter_image}'",
        )
