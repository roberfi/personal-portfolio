"""Tests for the PREPEND_WWW canonical domain redirect behaviour."""

from __future__ import annotations

from django.test import Client, TestCase, override_settings

_TEST_HOSTS = ["roberfi.com", "www.roberfi.com"]


@override_settings(PREPEND_WWW=True, ALLOWED_HOSTS=_TEST_HOSTS)
class TestPrependWwwEnabled(TestCase):
    """When PREPEND_WWW=True, non-www requests redirect permanently to www."""

    def test_non_www_redirects_to_www(self) -> None:
        response = Client().get("/en/", HTTP_HOST="roberfi.com")
        self.assertEqual(
            response.status_code,
            301,
            msg="Non-www request should return 301 when PREPEND_WWW is enabled",
        )

    def test_redirect_target_is_www(self) -> None:
        response = Client().get("/en/", HTTP_HOST="roberfi.com")
        location = response.get("Location", "")
        self.assertIn(
            "www.roberfi.com",
            location,
            msg=f"Redirect Location should contain 'www.roberfi.com', got '{location}'",
        )

    def test_www_request_is_not_redirected(self) -> None:
        response = Client().get("/en/", HTTP_HOST="www.roberfi.com")
        self.assertNotEqual(
            response.status_code,
            301,
            msg="www request should not be redirected when PREPEND_WWW is enabled",
        )

    def test_path_is_preserved_in_redirect(self) -> None:
        response = Client().get("/en/contact/", HTTP_HOST="roberfi.com")
        location = response.get("Location", "")
        self.assertIn(
            "/en/contact/",
            location,
            msg=f"Redirect should preserve the original path, got '{location}'",
        )


@override_settings(PREPEND_WWW=False, ALLOWED_HOSTS=_TEST_HOSTS)
class TestPrependWwwDisabled(TestCase):
    """When PREPEND_WWW=False (default), non-www requests are served normally."""

    def test_non_www_request_is_not_redirected(self) -> None:
        response = Client().get("/en/", HTTP_HOST="roberfi.com", follow=False)
        self.assertNotEqual(
            response.status_code,
            301,
            msg="Non-www request should not be redirected when PREPEND_WWW is disabled",
        )
