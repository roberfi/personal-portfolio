"""Tests for reCAPTCHA integration in contact view."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ContextManager
from unittest import mock

import requests
from bs4 import Tag
from django.conf import settings
from django.core import mail
from django.test import override_settings

import contact.tests.test_views.utils.constants as test_view_constants
from contact.models import ContactMessage
from contact.tests.test_views.base_view_test import BaseContactViewTest
from utils.test_utils.base_view_test_case import get_beautiful_soup_from_response
from utils.test_utils.constants import HtmlTag, Language

if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BaseTestRecaptcha(BaseContactViewTest):
    """Base class for testing reCAPTCHA functionality."""

    request_path = "contact/"
    use_recaptcha_token: bool  # Whether to include recaptcha_token in form data
    recaptcha_test_token = "test_token_12345"

    @classmethod
    def _get_form_data(cls) -> dict[str, Any]:
        """Get form data for POST requests, optionally including reCAPTCHA token."""
        data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        # Only add token if explicitly enabled (avoid AttributeError if not defined)
        if getattr(cls, "use_recaptcha_token", False):
            data["recaptcha_token"] = cls.recaptcha_test_token

        return data

    def _send_request(self) -> _MonkeyPatchedWSGIResponse:
        return self.client.post(f"/{self.language}/{self.request_path}", data=self._get_form_data(), follow=True)

    @classmethod
    def _create_mock_recaptcha_response(cls, *, success: bool, score: float, action: str) -> ContextManager[Any]:
        """Create a mock for the reCAPTCHA API response.

        Args:
            success: Whether the API should return success=true or false.
            score: The score to return in the API response.
            action: The action to return in the API response.
        """
        mock_response = mock.Mock(["raise_for_status", "json"])
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": success,
            "score": score,
            "action": action,
        }
        return mock.patch("contact.views.requests.post", return_value=mock_response)

    def _assert_contact_message(
        self,
        *,
        expected_count: int,
        expected_score: float | None = None,
    ) -> None:
        """Assert ContactMessage model state with default test data.

        Args:
            expected_count: Expected number of messages in database.
            expected_score: Expected reCAPTCHA score (None if not set).
        """

        self.assertEqual(
            ContactMessage.objects.count(),
            expected_count,
            msg="ContactMessage count should match expected value",
        )

        if expected_count == 0:
            return None

        message = ContactMessage.objects.first()
        assert message is not None, "No ContactMessage found"

        # Verify message contains expected test data
        self.assertEqual(message.name, test_view_constants.TEST_NAME, msg="Name field should match test data")
        self.assertEqual(message.email, test_view_constants.TEST_EMAIL, msg="Email field should match test data")
        self.assertEqual(message.subject, test_view_constants.TEST_SUBJECT, msg="Subject field should match test data")
        self.assertEqual(message.message, test_view_constants.TEST_MESSAGE, msg="Message field should match test data")
        self.assertEqual(message.is_read, False, msg="Message should not be marked as read")
        self.assertEqual(message.error, "", msg="Error field should be empty")
        self.assertIsNotNone(message.created_at, msg="Created timestamp should be set")

        # Verify reCAPTCHA score
        if expected_score is None:
            self.assertIsNone(message.recaptcha_score, msg="reCAPTCHA score should not be set")
        else:
            assert message.recaptcha_score is not None, "reCAPTCHA score should be set"
            self.assertAlmostEqual(
                message.recaptcha_score,
                expected_score,
                places=2,
                msg=f"reCAPTCHA score should be approximately {expected_score}",
            )

    def _assert_error_alert_displayed(self, soup: Tag) -> None:
        """Assert that the reCAPTCHA verification error alert is displayed with the localized message.

        Args:
            soup: The BeautifulSoup parsed HTML.
        """
        alerts = self._find_element_by_id(soup, test_view_constants.CONTACT_RESPONSE_ALERTS_ID)
        error_alert = self._find_element_by_tag_and_attribute(alerts, HtmlTag.DIV, "class", "alert-error")
        self._assert_text_of_element(error_alert, test_view_constants.RECAPTCHA_VERIFICATION_FAILED[self.language])

    def _assert_success_message_displayed(self, soup: Tag) -> None:
        """Assert that the success alert is displayed with the localized message.

        Args:
            soup: The BeautifulSoup parsed HTML.
        """
        alerts = self._find_element_by_id(soup, test_view_constants.CONTACT_RESPONSE_ALERTS_ID)
        success_alert = self._find_element_by_tag_and_attribute(alerts, HtmlTag.DIV, "class", "alert-success")
        self._assert_text_of_element(success_alert, test_view_constants.SUCCESS_MESSAGE[self.language])


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class _BaseTestRecaptchaNotConfigured(BaseTestRecaptcha):
    """Base class for testing reCAPTCHA when not configured (development mode)."""

    def test_form_submission_without_recaptcha_config(self) -> None:
        """Test that form works without reCAPTCHA configuration.

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with correct data
        self._assert_contact_message(
            expected_count=1,
            expected_score=None,  # No score when reCAPTCHA not configured
        )

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent")

    def test_recaptcha_not_loaded_in_template(self) -> None:
        """Test that reCAPTCHA script is not loaded when not configured."""
        response = self.client.get(f"/{self.language}/{self.request_path}")
        soup = get_beautiful_soup_from_response(response)

        # Check that reCAPTCHA script is not present
        recaptcha_script = soup.find("script", src=lambda x: x and "google.com/recaptcha" in x)
        self.assertIsNone(recaptcha_script, "reCAPTCHA script should not be loaded when not configured")

        # Check that hidden recaptcha_token field is not present
        recaptcha_input = soup.find("input", {"id": "id_recaptcha_token"})
        self.assertIsNone(recaptcha_input, "reCAPTCHA token input should not be present when not configured")


@override_settings(
    IS_RECAPTCHA_CONFIGURED=True,
    RECAPTCHA_SITE_KEY="test_site_key_12345",
    RECAPTCHA_SECRET_KEY="test_secret_key_67890",
    RECAPTCHA_SCORE_THRESHOLD=0.5,
)
class _BaseTestRecaptchaConfigured(BaseTestRecaptcha):
    """Base class for testing reCAPTCHA when configured."""

    def test_recaptcha_loaded_in_template(self) -> None:
        """Test that reCAPTCHA script is loaded when configured."""
        response = self.client.get(f"/{self.language}/{self.request_path}")
        soup = get_beautiful_soup_from_response(response)

        # Check that reCAPTCHA script is present
        recaptcha_script = soup.find("script", src=lambda x: x and "google.com/recaptcha" in x)
        self.assertIsNotNone(recaptcha_script, "reCAPTCHA script should be loaded when configured")
        assert isinstance(recaptcha_script, Tag)
        self.assertIn(
            "test_site_key_12345",
            recaptcha_script.get("src", ""),
            msg="reCAPTCHA script should contain site key",
        )

        # Check that hidden recaptcha_token field is present
        recaptcha_input = soup.find("input", {"id": "id_recaptcha_token"})
        self.assertIsNotNone(recaptcha_input, "reCAPTCHA token input should be present when configured")


class _BaseTestRecaptchaSuccess(_BaseTestRecaptchaConfigured):
    """Tests for successful reCAPTCHA verification with high score."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(success=True, score=0.9, action="contact_form")

    def test_successful_recaptcha_verification(self) -> None:
        """Test successful form submission with valid reCAPTCHA token.

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with score
        self._assert_contact_message(expected_count=1, expected_score=0.9)

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent")

        # Check the reCAPTCHA verification request was sent with the expected payload
        self.mocked_request.assert_called_once_with(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": self.recaptcha_test_token,
            },
            timeout=5,
        )


class _BaseTestRecaptchaLowScore(_BaseTestRecaptchaConfigured):
    """Tests for reCAPTCHA verification with low score."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(success=True, score=0.3, action="contact_form")

    def test_recaptcha_verification_low_score(self) -> None:
        """Test form submission with low reCAPTCHA score.

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent on low score")


class _BaseTestRecaptchaMissingToken(_BaseTestRecaptchaConfigured):
    """Tests for form submission without reCAPTCHA token."""

    def test_recaptcha_verification_missing_token(self) -> None:
        """Test form submission without reCAPTCHA token.

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent when token is missing")


class _BaseTestRecaptchaWrongAction(_BaseTestRecaptchaConfigured):
    """Tests for reCAPTCHA verification with wrong action."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(success=True, score=0.9, action="wrong_action")

    def test_recaptcha_verification_wrong_action(self) -> None:
        """Test form submission with wrong action in reCAPTCHA response.

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent when action doesn't match")


class _BaseTestRecaptchaApiFailure(_BaseTestRecaptchaConfigured):
    """Tests for reCAPTCHA API returning success=false."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(success=False, score=0.0, action="contact_form")

    def test_recaptcha_verification_api_success_false(self) -> None:
        """Test form submission when reCAPTCHA API returns success=false.

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent when API returns success=false")


class _BaseTestRecaptchaNetworkFailure(_BaseTestRecaptchaConfigured):
    """Tests for network errors (fail open)."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override to simulate network error."""
        return mock.patch("contact.views.requests.post", side_effect=requests.RequestException("Network error"))

    def test_recaptcha_network_error_allows_submission(self) -> None:
        """Test that network errors allow submission (fail open).

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully (fail open policy)
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with no score (API unreachable)
        self._assert_contact_message(
            expected_count=1,
            expected_score=None,
        )

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent (fail open policy)")


class _BaseTestRecaptchaTimeout(_BaseTestRecaptchaConfigured):
    """Tests for API timeout (fail open)."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override to simulate timeout."""
        return mock.patch("contact.views.requests.post", side_effect=requests.Timeout("Request timeout"))

    def test_recaptcha_timeout_allows_submission(self) -> None:
        """Test that API timeout allows submission (fail open).

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully (fail open policy)
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with no score (timeout)
        self._assert_contact_message(
            expected_count=1,
            expected_score=None,
        )

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent (fail open policy)")


class _BaseTestRecaptchaUnexpectedFailure(_BaseTestRecaptchaConfigured):
    """Tests for unexpected errors (fail closed)."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override to simulate unexpected error."""
        return mock.patch("contact.views.requests.post", side_effect=ValueError("Unexpected error"))

    def test_recaptcha_unexpected_error_rejects_submission(self) -> None:
        """Test that unexpected errors reject submission (fail closed).

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent on unexpected error (fail closed)")


class _BaseTestRecaptchaHttpFailure(_BaseTestRecaptchaConfigured):
    """Tests for HTTP errors (fail open)."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        """Override to simulate HTTP error."""
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        return mock.patch("contact.views.requests.post", return_value=mock_response)

    def test_recaptcha_api_http_error(self) -> None:
        """Test handling of HTTP errors from reCAPTCHA API.

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully (fail open for network errors)
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with no score (API error)
        self._assert_contact_message(
            expected_count=1,
            expected_score=None,
        )

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent (fail open policy)")


class _BaseTestRecaptchaScoreAtThreshold(_BaseTestRecaptchaConfigured):
    """Tests for score exactly at threshold."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(
            success=True,
            score=0.5,
            action="contact_form",
        )

    def test_recaptcha_score_at_threshold(self) -> None:
        """Test form submission with reCAPTCHA score exactly at threshold.

        Uses response_data from setUp which made the POST request.
        """
        # Should redirect successfully (>= threshold)
        self._assert_reponse_status_code(expected_status_code=200)

        # Check success message is displayed
        self._assert_success_message_displayed(self.response_data.soup)

        # Check message was saved with score at threshold
        self._assert_contact_message(
            expected_count=1,
            expected_score=0.5,
        )

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1, msg="One email should be sent (score at threshold)")


class _BaseTestRecaptchaScoreBelowThreshold(_BaseTestRecaptchaConfigured):
    """Tests for score just below threshold."""

    use_recaptcha_token = True

    @classmethod
    def _mock_on_request(cls) -> ContextManager[Any]:
        return cls._create_mock_recaptcha_response(
            success=True,
            score=0.49,
            action="contact_form",
        )

    def test_recaptcha_score_just_below_threshold(self) -> None:
        """Test form submission with reCAPTCHA score just below threshold.

        Uses response_data from setUp which made the POST request.
        """
        # Should not redirect, should show error
        self._assert_reponse_status_code(expected_status_code=200)

        # Check error message is displayed
        self._assert_error_alert_displayed(self.response_data.soup)

        # Check no message was saved
        self._assert_contact_message(expected_count=0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0, msg="No email should be sent when score below threshold")


# Concrete test classes for each scenario in English
class TestRecaptchaSuccessEnglish(_BaseTestRecaptchaSuccess):
    """Test successful reCAPTCHA in English."""

    language = Language.ENGLISH


class TestRecaptchaLowScoreEnglish(_BaseTestRecaptchaLowScore):
    """Test low score reCAPTCHA in English."""

    language = Language.ENGLISH


class TestRecaptchaMissingTokenEnglish(_BaseTestRecaptchaMissingToken):
    """Test missing token in English."""

    language = Language.ENGLISH


class TestRecaptchaWrongActionEnglish(_BaseTestRecaptchaWrongAction):
    """Test wrong action in English."""

    language = Language.ENGLISH


class TestRecaptchaApiFailureEnglish(_BaseTestRecaptchaApiFailure):
    """Test API failure in English."""

    language = Language.ENGLISH


class TestRecaptchaNetworkErrorEnglish(_BaseTestRecaptchaNetworkFailure):
    """Test network error in English."""

    language = Language.ENGLISH


class TestRecaptchaTimeoutEnglish(_BaseTestRecaptchaTimeout):
    """Test timeout in English."""

    language = Language.ENGLISH


class TestRecaptchaUnexpectedErrorEnglish(_BaseTestRecaptchaUnexpectedFailure):
    """Test unexpected error in English."""

    language = Language.ENGLISH


class TestRecaptchaHttpErrorEnglish(_BaseTestRecaptchaHttpFailure):
    """Test HTTP error in English."""

    language = Language.ENGLISH


class TestRecaptchaScoreAtThresholdEnglish(_BaseTestRecaptchaScoreAtThreshold):
    """Test score at threshold in English."""

    language = Language.ENGLISH


class TestRecaptchaScoreBelowThresholdEnglish(_BaseTestRecaptchaScoreBelowThreshold):
    """Test score below threshold in English."""

    language = Language.ENGLISH


# Concrete test classes for each scenario in Spanish
class TestRecaptchaSuccessSpanish(_BaseTestRecaptchaSuccess):
    """Test successful reCAPTCHA in Spanish."""

    language = Language.SPANISH


class TestRecaptchaLowScoreSpanish(_BaseTestRecaptchaLowScore):
    """Test low score reCAPTCHA in Spanish."""

    language = Language.SPANISH


class TestRecaptchaMissingTokenSpanish(_BaseTestRecaptchaMissingToken):
    """Test missing token in Spanish."""

    language = Language.SPANISH


class TestRecaptchaWrongActionSpanish(_BaseTestRecaptchaWrongAction):
    """Test wrong action in Spanish."""

    language = Language.SPANISH


class TestRecaptchaApiFailureSpanish(_BaseTestRecaptchaApiFailure):
    """Test API failure in Spanish."""

    language = Language.SPANISH


class TestRecaptchaNetworkErrorSpanish(_BaseTestRecaptchaNetworkFailure):
    """Test network error in Spanish."""

    language = Language.SPANISH


class TestRecaptchaTimeoutSpanish(_BaseTestRecaptchaTimeout):
    """Test timeout in Spanish."""

    language = Language.SPANISH


class TestRecaptchaUnexpectedErrorSpanish(_BaseTestRecaptchaUnexpectedFailure):
    """Test unexpected error in Spanish."""

    language = Language.SPANISH


class TestRecaptchaHttpErrorSpanish(_BaseTestRecaptchaHttpFailure):
    """Test HTTP error in Spanish."""

    language = Language.SPANISH


class TestRecaptchaScoreAtThresholdSpanish(_BaseTestRecaptchaScoreAtThreshold):
    """Test score at threshold in Spanish."""

    language = Language.SPANISH


class TestRecaptchaScoreBelowThresholdSpanish(_BaseTestRecaptchaScoreBelowThreshold):
    """Test score below threshold in Spanish."""

    language = Language.SPANISH


class TestRecaptchaNotConfiguredEnglish(_BaseTestRecaptchaNotConfigured):
    """Test reCAPTCHA when not configured in English."""

    language = Language.ENGLISH


class TestRecaptchaNotConfiguredSpanish(_BaseTestRecaptchaNotConfigured):
    """Test reCAPTCHA when not configured in Spanish."""

    language = Language.SPANISH
