"""Tests for the SECURE_PROXY_SSL_HEADER / X-Forwarded-Proto configuration."""

from __future__ import annotations

from django.test import RequestFactory, TestCase, override_settings


class TestSecureProxyHeaderEnabled(TestCase):
    """When SECURE_PROXY_SSL_HEADER is set (production, DEBUG=False), Django trusts X-Forwarded-Proto."""

    @override_settings(SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"))
    def test_request_is_secure_with_https_header(self) -> None:
        request = RequestFactory().get("/", HTTP_X_FORWARDED_PROTO="https")
        self.assertTrue(
            request.is_secure(),
            msg="request.is_secure() should be True when X-Forwarded-Proto: https is trusted",
        )

    @override_settings(SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"))
    def test_absolute_uri_uses_https_with_header(self) -> None:
        request = RequestFactory().get("/en/", HTTP_X_FORWARDED_PROTO="https")
        uri = request.build_absolute_uri()
        self.assertTrue(
            uri.startswith("https://"),
            msg=f"build_absolute_uri() should return https:// URL, got '{uri}'",
        )

    @override_settings(SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"))
    def test_request_is_not_secure_with_http_header(self) -> None:
        request = RequestFactory().get("/", HTTP_X_FORWARDED_PROTO="http")
        self.assertFalse(
            request.is_secure(),
            msg="request.is_secure() should be False when X-Forwarded-Proto: http",
        )


class TestSecureProxyHeaderDisabled(TestCase):
    """When SECURE_PROXY_SSL_HEADER is absent (development, DEBUG=True), X-Forwarded-Proto is ignored."""

    @override_settings(SECURE_PROXY_SSL_HEADER=None)
    def test_x_forwarded_proto_header_is_ignored(self) -> None:
        request = RequestFactory().get("/", HTTP_X_FORWARDED_PROTO="https")
        self.assertFalse(
            request.is_secure(),
            msg="request.is_secure() should be False when SECURE_PROXY_SSL_HEADER is not set",
        )
