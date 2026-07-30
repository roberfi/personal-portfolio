from __future__ import annotations

from django.test import RequestFactory, TestCase, override_settings

from utils.helpers import get_canonical_base_url


class TestGetCanonicalBaseUrl(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/", SERVER_NAME="testserver")

    @override_settings(CANONICAL_HOST="")
    def test_falls_back_to_request_when_unset(self) -> None:
        self.assertEqual(
            returned := get_canonical_base_url(self.request),
            expected := "http://testserver",
            f"Expected '{expected}' when CANONICAL_HOST is unset, got '{returned}'",
        )

    @override_settings(CANONICAL_HOST="www.example.com")
    def test_uses_canonical_host_when_set(self) -> None:
        self.assertEqual(
            returned := get_canonical_base_url(self.request),
            expected := "https://www.example.com",
            f"Expected '{expected}' when CANONICAL_HOST is set, got '{returned}'",
        )

    @override_settings(CANONICAL_HOST="www.example.com")
    def test_ignores_request_host_when_canonical_host_is_set(self) -> None:
        request = RequestFactory().get("/", SERVER_NAME="some-other-host")
        self.assertEqual(
            returned := get_canonical_base_url(request),
            expected := "https://www.example.com",
            f"Expected the request's host to be ignored in favor of '{expected}', got '{returned}'",
        )
