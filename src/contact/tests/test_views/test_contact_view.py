"""Tests for contact view."""

from __future__ import annotations

from unittest import mock

from bs4 import Tag
from django.core import mail
from django.test import override_settings

import contact.tests.test_views.utils.constants as test_view_constants
import home.tests.test_views.utils.constants as home_test_view_constants
import utils.test_utils.constants as common_constants
from base.models import LegalAndPrivacy, SiteMedia
from contact.models import ContactFormConfiguration, ContactMessage
from contact.tests.test_views.base_view_test import BaseContactViewTest
from home.models import Service
from utils.test_utils import base_view_test_case
from utils.test_utils.base_view_test_case import ElementText, get_beautiful_soup_from_response
from utils.test_utils.constants import ATTR_PLACEHOLDER, HtmlTag, Language


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class BaseTestContactViewContent(base_view_test_case.CommonPageTestsMixin, BaseContactViewTest):
    """Base class for testing contact view content."""

    request_path = "contact/"

    @classmethod
    def init_db(cls) -> None:
        """Initialize database - no specific data needed for contact page."""
        pass

    def test_response(self) -> None:
        """Test that the contact page loads successfully."""
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("contact.html")
        self._assert_template_is_used("cotton/base.html")

    def test_json_ld_contact_page_schema(self) -> None:
        """Test that contact view includes valid JSON-LD ContactPage schema."""
        data = self._get_json_ld_data()

        # Verify @context structure
        self.assertIn("@context", data, f"Expected '@context' key in the JSON-LD data, got keys: {list(data)}")
        self.assertIsInstance(
            data["@context"], dict, f"Expected '@context' to be a dict, got '{type(data['@context'])}'"
        )
        self.assertEqual(
            vocab := data["@context"]["@vocab"],
            "https://schema.org/",
            f"Expected '@context.@vocab' to be 'https://schema.org/', got '{vocab}'",
        )

        # Verify language
        self.assertEqual(
            language := data["@context"]["@language"],
            self.language,
            f"Expected '@context.@language' to be '{self.language}', got '{language}'",
        )

        # Verify @type
        self.assertEqual(type_ := data["@type"], "ContactPage", f"Expected '@type' to be 'ContactPage', got '{type_}'")

        # Verify fields
        self.assertEqual(
            name := data["name"],
            expected_name := test_view_constants.META_TITLE[self.language],
            f"Expected 'name' to be '{expected_name}', got '{name}'",
        )
        self.assertEqual(
            description := data["description"],
            expected_description := test_view_constants.META_DESCRIPTION[self.language],
            f"Expected 'description' to be '{expected_description}', got '{description}'",
        )

    def test_meta_tags(self) -> None:
        """Test that meta tags have correct values for contact page."""
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            test_view_constants.META_KEYWORDS[self.language],
        )

    def test_seo_open_graph_tags(self) -> None:
        """Test that Open Graph tags have correct values."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            test_view_constants.META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            test_view_constants.META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().og_preview_image_display.url}",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/contact/",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:type"),
            "content",
            "profile",
        )

    def test_seo_twitter_card(self) -> None:
        """Test that Twitter card meta tags have correct values."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:card"),
            "content",
            "summary_large_image",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            test_view_constants.META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            test_view_constants.META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:image"),
            "content",
            f"http://testserver{SiteMedia.get_solo().twitter_preview_image_display.url}",
        )

    def __check_the_elements_in_contact_container(self, contact_container: Tag) -> None:
        self._assert_text_of_elements(
            contact_container,
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.CONTACT_TITLE_ID,
                expected_text=test_view_constants.CONTACT_PAGE_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.P,
                element_id="contact-description",
                expected_text=test_view_constants.CONTACT_PAGE_DESCRIPTION[self.language],
            ),
        )

        form = self._find_element_by_tag_and_id(contact_container, HtmlTag.FORM, test_view_constants.CONTACT_FORM_ID)

        self._assert_text_of_element_by_tag_and_id(
            form,
            HtmlTag.LABEL,
            test_view_constants.CONTACT_FORM_NAME_LABEL_ID,
            expected_text=test_view_constants.LABEL_NAME_TEXT[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(form, HtmlTag.INPUT, test_view_constants.CONTACT_FORM_NAME_ID),
            ATTR_PLACEHOLDER,
            test_view_constants.INPUT_NAME_PLACEHOLDER[self.language],
        )

        self._assert_text_of_element_by_tag_and_id(
            form,
            HtmlTag.LABEL,
            test_view_constants.CONTACT_FORM_EMAIL_LABEL_ID,
            expected_text=test_view_constants.LABEL_EMAIL_TEXT[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(form, HtmlTag.INPUT, test_view_constants.CONTACT_FORM_EMAIL_ID),
            ATTR_PLACEHOLDER,
            test_view_constants.INPUT_EMAIL_PLACEHOLDER[self.language],
        )

        self._assert_text_of_element_by_tag_and_id(
            form,
            HtmlTag.LABEL,
            test_view_constants.CONTACT_FORM_SUBJECT_LABEL_ID,
            expected_text=test_view_constants.LABEL_SUBJECT_TEXT[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(form, HtmlTag.INPUT, test_view_constants.CONTACT_FORM_SUBJECT_ID),
            ATTR_PLACEHOLDER,
            test_view_constants.INPUT_SUBJECT_PLACEHOLDER[self.language],
        )

        self._assert_text_of_element_by_tag_and_id(
            form,
            HtmlTag.LABEL,
            test_view_constants.CONTACT_FORM_MESSAGE_LABEL_ID,
            expected_text=test_view_constants.LABEL_MESSAGE_TEXT[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(form, HtmlTag.TEXTAREA, test_view_constants.CONTACT_FORM_MESSAGE_ID),
            ATTR_PLACEHOLDER,
            test_view_constants.INPUT_MESSAGE_PLACEHOLDER[self.language],
        )

        self._assert_text_of_element_by_tag_and_id(
            form,
            HtmlTag.BUTTON,
            test_view_constants.CONTACT_FORM_SUBMIT_BUTTON_ID,
            expected_text=test_view_constants.SUBMIT_BUTTON_TEXT[self.language],
        )

        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.P,
            test_view_constants.CONTACT_ADDITIONAL_INFO_ID,
            expected_text=test_view_constants.ADDITIONAL_INFO_TEXT[self.language],
        )

    def test_contact_page_elements(self) -> None:
        """Test that the contact page contains the correct elements."""
        self.__check_the_elements_in_contact_container(
            self._find_element_by_tag_and_id(
                self.response_data.soup, HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
            )
        )

    def test_no_privacy_policy_checkbox_by_default(self) -> None:
        """Test that no privacy policy consent checkbox is shown when no privacy notice is configured."""
        contact_container = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        self._assert_element_not_exists(contact_container, test_view_constants.CONTACT_FORM_PRIVACY_POLICY_ID)

    def test_valid_form_submission(self) -> None:
        """Test successful form submission."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        with mock.patch(
            "django.utils.timezone.now",
            # get_datetime_with_mocked_now(test_view_constants.MOCKED_NOW),
            mock.Mock(return_value=test_view_constants.MOCKED_NOW),
        ):
            response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        # Check redirect after successful submission
        self.assertRedirects(response, f"/{self.language}/{self.request_path}", status_code=302, target_status_code=200)

        # Check message was saved to database
        self.assertEqual(ContactMessage.objects.count(), 1, "ContactMessage was not created in the database")
        message = ContactMessage.objects.first()

        assert message is not None, "ContactMessage retrieved from database is None"

        self.assertEqual(
            message.name,
            test_view_constants.TEST_NAME,
            f"Name field mismatch: expected '{test_view_constants.TEST_NAME}', got '{message.name}'",
        )
        self.assertEqual(
            message.email,
            test_view_constants.TEST_EMAIL,
            f"Email field mismatch: expected '{test_view_constants.TEST_EMAIL}', got '{message.email}'",
        )
        self.assertEqual(
            message.subject,
            test_view_constants.TEST_SUBJECT,
            f"Subject field mismatch: expected '{test_view_constants.TEST_SUBJECT}', got '{message.subject}'",
        )
        self.assertEqual(
            message.message,
            test_view_constants.TEST_MESSAGE,
            f"Message field mismatch: expected '{test_view_constants.TEST_MESSAGE}', got '{message.message}'",
        )
        self.assertEqual(
            message.created_at,
            test_view_constants.MOCKED_NOW,
            f"Created_at field mismatch: expected '{test_view_constants.MOCKED_NOW}', got '{message.created_at}'",
        )
        self.assertFalse(
            message.is_read,
            "is_read field should be False for new messages",
        )
        self.assertEqual(
            message.error,
            "",
            "Error field should be empty for valid submissions",
        )

        # Check email was sent
        self.assertEqual(
            outbox_len := len(mail.outbox), 1, f"Expected exactly one email to be sent, got '{outbox_len}'"
        )
        self.assertEqual(
            mail.outbox[0].to,
            [test_view_constants.TO_EMAIL_ADDRESS],
            f"Email to address mismatch: expected '{test_view_constants.TO_EMAIL_ADDRESS}', got '{mail.outbox[0].to}'",
        )
        self.assertEqual(
            mail.outbox[0].from_email,
            test_view_constants.FROM_EMAIL_ADDRESS,
            (
                f"Email from address mismatch: expected '{test_view_constants.FROM_EMAIL_ADDRESS}',"
                f" got '{mail.outbox[0].from_email}'"
            ),
        )
        self.assertEqual(
            mail.outbox[0].reply_to,
            [test_view_constants.TEST_EMAIL],
            f"Email reply-to mismatch: expected '{test_view_constants.TEST_EMAIL}', got '{mail.outbox[0].reply_to}'",
        )

        expected_subject = f"[Portfolio Contact] {test_view_constants.TEST_SUBJECT}"
        self.assertEqual(
            mail.outbox[0].subject,
            expected_subject,
            f"Email subject mismatch: expected '{expected_subject}', got '{mail.outbox[0].subject}'",
        )

        expected_body = test_view_constants.EMAIL_BODY_TEMPLATE.format(
            name=test_view_constants.TEST_NAME,
            email=test_view_constants.TEST_EMAIL,
            subject=test_view_constants.TEST_SUBJECT,
            message=test_view_constants.TEST_MESSAGE,
        )

        self.assertEqual(
            mail.outbox[0].body,
            expected_body,
            f"Email body mismatch: expected '{expected_body}', got '{mail.outbox[0].body}'",
        )

    def test_contact_page_after_submission(self) -> None:
        """Test that success message is displayed after valid submission."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        # Submit form and follow redirect
        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data, follow=True)

        contact_container = self._find_element_by_tag_and_id(
            get_beautiful_soup_from_response(response), HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )
        response_alerts = self._find_element_by_tag_and_id(
            contact_container, HtmlTag.DIV, test_view_constants.CONTACT_RESPONSE_ALERTS_ID
        ).find_all("div", class_="alert")

        self.assertEqual(
            len(response_alerts),
            1,
            f"There should be exactly one alert message displayed, found {len(response_alerts)}",
        )

        response_alert = response_alerts[0]
        self._assert_element_contains_class_name(response_alert, "alert-success")
        self._assert_text_of_element(response_alert, test_view_constants.SUCCESS_MESSAGE[self.language])

        self.__check_the_elements_in_contact_container(contact_container)

    def test_invalid_form_invalid_email(self) -> None:
        """Test form submission with invalid email."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_INVALID_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        # Should not redirect, should show form with errors
        self.assertEqual(
            status_code := response.status_code,
            200,
            f"Expected status code 200 when the form is invalid, got '{status_code}'",
        )

        # Check no message was saved
        self.assertEqual(
            message_count := ContactMessage.objects.count(),
            0,
            f"Expected no ContactMessage to be created for an invalid submission, got '{message_count}'",
        )

        # Check no email was sent
        self.assertEqual(
            outbox_len := len(mail.outbox),
            0,
            f"Expected no email to be sent for an invalid submission, got '{outbox_len}'",
        )

        contact_container = self._find_element_by_tag_and_id(
            get_beautiful_soup_from_response(response), HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.SPAN,
            test_view_constants.CONTACT_FORM_EMAIL_ERROR_ID,
            expected_text=test_view_constants.VALIDATION_ERROR_INVALID_EMAIL[self.language],
        )

        self.__check_the_elements_in_contact_container(contact_container)

    def test_invalid_form_short_message(self) -> None:
        """Test form submission with message that's too short."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_SHORT_MESSAGE,
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        # Should not redirect, should show form with errors
        self.assertEqual(
            status_code := response.status_code,
            200,
            f"Expected status code 200 when the form is invalid, got '{status_code}'",
        )

        # Check no message was saved
        self.assertEqual(
            message_count := ContactMessage.objects.count(),
            0,
            f"Expected no ContactMessage to be created for an invalid submission, got '{message_count}'",
        )

        # Check no email was sent
        self.assertEqual(
            outbox_len := len(mail.outbox),
            0,
            f"Expected no email to be sent for an invalid submission, got '{outbox_len}'",
        )

        contact_container = self._find_element_by_tag_and_id(
            get_beautiful_soup_from_response(response), HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.SPAN,
            test_view_constants.CONTACT_FORM_MESSAGE_ERROR_ID,
            expected_text=test_view_constants.VALIDATION_ERROR_SHORT_MESSAGE[self.language],
        )

        self.__check_the_elements_in_contact_container(contact_container)

    def test_email_sending_error(self) -> None:
        """Test that email sending errors are handled gracefully."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        # Mock EmailMessage.send to raise an exception
        with mock.patch(
            "contact.views.EmailMessage.send", side_effect=Exception(test_view_constants.MOCKED_ERROR_MESSAGE)
        ):
            response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        # Should still redirect (user shouldn't see the error)
        self.assertRedirects(response, f"/{self.language}/{self.request_path}", status_code=302, target_status_code=200)

        # Check message was saved to database
        self.assertEqual(ContactMessage.objects.count(), 1, "ContactMessage was not created in the database")
        message = ContactMessage.objects.first()

        assert message is not None, "ContactMessage retrieved from database is None"

        # Check the basic fields are correct
        self.assertEqual(
            message.name,
            test_view_constants.TEST_NAME,
            f"Name field mismatch: expected '{test_view_constants.TEST_NAME}', got '{message.name}'",
        )
        self.assertEqual(
            message.email,
            test_view_constants.TEST_EMAIL,
            f"Email field mismatch: expected '{test_view_constants.TEST_EMAIL}', got '{message.email}'",
        )
        self.assertEqual(
            message.subject,
            test_view_constants.TEST_SUBJECT,
            f"Subject field mismatch: expected '{test_view_constants.TEST_SUBJECT}', got '{message.subject}'",
        )
        self.assertEqual(
            message.message,
            test_view_constants.TEST_MESSAGE,
            f"Message field mismatch: expected '{test_view_constants.TEST_MESSAGE}', got '{message.message}'",
        )
        self.assertFalse(message.is_read, f"is_read field should be False for new messages, got '{message.is_read}'")

        # Check that the error was saved
        self.assertNotEqual(
            message.error,
            "",
            "Error field should contain the exception details when email sending fails",
        )
        self.assertIn(
            test_view_constants.MOCKED_ERROR_MESSAGE,
            message.error,
            f"Error field should contain the exception message, found: '{message.error}'",
        )
        self.assertIn(
            "Traceback",
            message.error,
            "Error field should contain the full traceback for debugging",
        )

        # Check that no email was sent (since send() was mocked to fail)
        self.assertEqual(len(mail.outbox), 0, "No email should have been sent when send() raises an exception")


class TestContactViewContentEnglish(BaseTestContactViewContent):
    """Test contact view content in English."""

    language = Language.ENGLISH


class TestContactViewContentSpanish(BaseTestContactViewContent):
    """Test contact view content in Spanish."""

    language = Language.SPANISH


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class BaseTestContactViewPrivacyPolicy(BaseContactViewTest):
    """Base class for testing the contact view privacy policy consent checkbox."""

    request_path = "contact/"

    @classmethod
    def init_db(cls) -> None:
        """Configure the ContactFormConfiguration to use the first Legal and Privacy section as the privacy policy."""
        legal_and_privacy = LegalAndPrivacy.objects.get(
            title=home_test_view_constants.LEGAL_SECTION_1[Language.ENGLISH]
        )

        privacy_notice = ContactFormConfiguration.get_solo()
        ContactFormConfiguration.objects.filter(pk=privacy_notice.pk).update(legal_and_privacy=legal_and_privacy)

    def __get_privacy_policy_form_control(self) -> Tag:
        contact_container = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        return self._find_element_by_tag_and_id(
            contact_container, HtmlTag.DIV, test_view_constants.CONTACT_FORM_PRIVACY_POLICY_ID
        )

    def test_privacy_policy_checkbox_is_shown(self) -> None:
        """Test that the privacy policy checkbox is shown and links to the configured Legal and Privacy section."""
        privacy_policy_control = self.__get_privacy_policy_form_control()

        checkbox = self._find_element_by_tag_and_id(
            privacy_policy_control, HtmlTag.INPUT, test_view_constants.CONTACT_FORM_PRIVACY_POLICY_CHECKBOX_ID
        )
        self._assert_attribute_of_element(checkbox, "type", "checkbox")

        self._assert_text_of_element(
            privacy_policy_control,
            f"{test_view_constants.PRIVACY_POLICY_LABEL_TEXT[self.language]}"
            f" {home_test_view_constants.LEGAL_SECTION_1[self.language]}",
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                privacy_policy_control, HtmlTag.BUTTON, test_view_constants.CONTACT_FORM_PRIVACY_POLICY_LINK_ID
            ),
            common_constants.ATTR_ONCLICK,
            f"{home_test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

    def test_submission_rejected_without_consent(self) -> None:
        """Test that the form submission is rejected if the privacy policy checkbox is not checked."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        self.assertEqual(
            status_code := response.status_code,
            200,
            f"Expected status code 200 when consent is not given, got '{status_code}'",
        )
        self.assertEqual(
            message_count := ContactMessage.objects.count(),
            0,
            f"Expected no ContactMessage to be created without consent, got '{message_count}'",
        )
        self.assertEqual(
            outbox_len := len(mail.outbox), 0, f"Expected no email to be sent without consent, got '{outbox_len}'"
        )

        contact_container = self._find_element_by_tag_and_id(
            get_beautiful_soup_from_response(response), HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.SPAN,
            test_view_constants.CONTACT_FORM_PRIVACY_POLICY_ERROR_ID,
            expected_text=test_view_constants.VALIDATION_ERROR_PRIVACY_POLICY_NOT_ACCEPTED[self.language],
        )

    def test_submission_accepted_with_consent(self) -> None:
        """Test that the form submission succeeds when the privacy policy checkbox is checked."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
            "privacy_policy_accepted": "on",
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        self.assertRedirects(response, f"/{self.language}/{self.request_path}", status_code=302, target_status_code=200)
        self.assertEqual(
            message_count := ContactMessage.objects.count(),
            1,
            f"Expected one ContactMessage to be created when consent is given, got '{message_count}'",
        )


class TestContactViewPrivacyPolicyEnglish(BaseTestContactViewPrivacyPolicy):
    """Test contact view privacy policy consent checkbox in English."""

    language = Language.ENGLISH


class TestContactViewPrivacyPolicySpanish(BaseTestContactViewPrivacyPolicy):
    """Test contact view privacy policy consent checkbox in Spanish."""

    language = Language.SPANISH


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class BaseTestContactViewIntro(BaseContactViewTest):
    """Base class for testing the configurable intro text on the contact page."""

    request_path = "contact/"

    @classmethod
    def init_db(cls) -> None:
        """Set a custom intro on the ContactFormConfiguration singleton."""
        config = ContactFormConfiguration.get_solo()
        ContactFormConfiguration.objects.filter(pk=config.pk).update(
            intro_en=test_view_constants.CONTACT_FORM_CUSTOM_INTRO[Language.ENGLISH],
            intro_es=test_view_constants.CONTACT_FORM_CUSTOM_INTRO[Language.SPANISH],
        )

    def test_custom_intro_is_shown(self) -> None:
        """Test that the custom intro text from the model is shown instead of the default."""
        contact_container = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        expected = test_view_constants.CONTACT_FORM_CUSTOM_INTRO[self.language]
        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.P,
            "contact-description",
            expected_text=expected,
        )

    def test_default_intro_is_shown_when_intro_is_empty(self) -> None:
        """Test that the default (translated) intro is shown when the model field is blank."""
        config = ContactFormConfiguration.get_solo()
        ContactFormConfiguration.objects.filter(pk=config.pk).update(intro_en="", intro_es="")

        response = self.client.get(f"/{self.language}/{self.request_path}")
        soup = get_beautiful_soup_from_response(response)
        contact_container = self._find_element_by_tag_and_id(
            soup, HtmlTag.DIV, test_view_constants.CONTACT_CONTAINER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            contact_container,
            HtmlTag.P,
            "contact-description",
            expected_text=test_view_constants.CONTACT_PAGE_DESCRIPTION[self.language],
        )


class TestContactViewIntroEnglish(BaseTestContactViewIntro):
    """Test configurable contact intro in English."""

    language = Language.ENGLISH


class TestContactViewIntroSpanish(BaseTestContactViewIntro):
    """Test configurable contact intro in Spanish."""

    language = Language.SPANISH


@override_settings(
    IS_RECAPTCHA_CONFIGURED=False,
    RECAPTCHA_SITE_KEY=None,
    RECAPTCHA_SECRET_KEY=None,
)
class BaseTestContactViewQualificationFields(BaseContactViewTest):
    """Base class for testing lead-qualification fields on the contact form."""

    request_path = "contact/"

    @classmethod
    def init_db(cls) -> None:
        Service.objects.create(
            title=test_view_constants.TEST_SERVICE_TITLE,
            title_es=test_view_constants.TEST_SERVICE_TITLE,
            slug=test_view_constants.TEST_SERVICE_SLUG,
            short_description="Test short description",
            short_description_es="Descripción corta de prueba",
            long_description="Test long description",
            long_description_es="Descripción larga de prueba",
            is_active=True,
        )
        Service.objects.create(
            title="Inactive Service",
            title_es="Servicio Inactivo",
            slug=test_view_constants.TEST_SERVICE_INACTIVE_SLUG,
            short_description="Inactive short description",
            short_description_es="Descripción inactiva",
            long_description="Inactive long description",
            long_description_es="Descripción larga inactiva",
            is_active=False,
        )

    def test_qualification_selects_are_rendered(self) -> None:
        """Test that service_interest, budget_range, and timeline select fields are in the form."""
        form = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.FORM, test_view_constants.CONTACT_FORM_ID
        )
        self._find_element_by_tag_and_id(form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_SERVICE_INTEREST_ID)
        self._find_element_by_tag_and_id(form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_BUDGET_RANGE_ID)
        self._find_element_by_tag_and_id(form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_TIMELINE_ID)

    def test_service_prefill_from_query_param(self) -> None:
        """Test that ?service=<slug> pre-selects the matching service in the form."""
        service = Service.objects.get(slug=test_view_constants.TEST_SERVICE_SLUG)

        response = self.client.get(
            f"/{self.language}/{self.request_path}?service={test_view_constants.TEST_SERVICE_SLUG}"
        )
        soup = get_beautiful_soup_from_response(response)
        form = self._find_element_by_tag_and_id(soup, HtmlTag.FORM, test_view_constants.CONTACT_FORM_ID)
        service_select = self._find_element_by_tag_and_id(
            form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_SERVICE_INTEREST_ID
        )

        service_option = service_select.find("option", {"value": str(service.pk)})
        assert isinstance(service_option, Tag), (
            f"Option for service pk={service.pk} not found in service_interest select"
        )

        self.assertIn(
            "selected",
            service_option.attrs,
            f"Service option should be selected for ?service={test_view_constants.TEST_SERVICE_SLUG}",
        )

    def test_invalid_service_slug_in_query_param_is_ignored(self) -> None:
        """Test that an unrecognised ?service= value leaves the field unselected."""
        response = self.client.get(f"/{self.language}/{self.request_path}?service=nonexistent-slug")
        self.assertEqual(response.status_code, 200, "Expected 200 with invalid service slug")
        soup = get_beautiful_soup_from_response(response)
        form = self._find_element_by_tag_and_id(soup, HtmlTag.FORM, test_view_constants.CONTACT_FORM_ID)
        service_select = self._find_element_by_tag_and_id(
            form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_SERVICE_INTEREST_ID
        )
        active_service = Service.objects.get(slug=test_view_constants.TEST_SERVICE_SLUG)
        service_option = service_select.find("option", {"value": str(active_service.pk)})
        assert isinstance(service_option, Tag), "Active service option should still appear in the list"
        self.assertNotIn(
            "selected",
            service_option.attrs,
            "Active service option should NOT be selected for an invalid slug",
        )

    def test_inactive_service_slug_in_query_param_is_ignored(self) -> None:
        """Test that an inactive service slug in ?service= leaves the field unselected."""
        response = self.client.get(
            f"/{self.language}/{self.request_path}?service={test_view_constants.TEST_SERVICE_INACTIVE_SLUG}"
        )
        self.assertEqual(response.status_code, 200, "Expected 200 with inactive service slug")
        soup = get_beautiful_soup_from_response(response)
        form = self._find_element_by_tag_and_id(soup, HtmlTag.FORM, test_view_constants.CONTACT_FORM_ID)
        service_select = self._find_element_by_tag_and_id(
            form, HtmlTag.SELECT, test_view_constants.CONTACT_FORM_SERVICE_INTEREST_ID
        )
        active_service = Service.objects.get(slug=test_view_constants.TEST_SERVICE_SLUG)
        service_option = service_select.find("option", {"value": str(active_service.pk)})
        assert isinstance(service_option, Tag), "Active service option should still appear in the list"
        self.assertNotIn(
            "selected",
            service_option.attrs,
            "Active service option should NOT be selected when an inactive slug is given",
        )

    def test_form_submission_with_qualification_fields(self) -> None:
        """Test that qualification fields are saved to the DB and appear in the notification email."""
        service = Service.objects.get(slug=test_view_constants.TEST_SERVICE_SLUG)

        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
            "service_interest": service.pk,
            "budget_range": test_view_constants.TEST_BUDGET_RANGE_VALUE,
            "timeline": test_view_constants.TEST_TIMELINE_VALUE,
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        self.assertRedirects(
            response,
            f"/{self.language}/{self.request_path}",
            status_code=302,
            target_status_code=200,
        )

        message = ContactMessage.objects.first()
        assert message is not None, "ContactMessage was not created"

        self.assertEqual(
            message.service_interest,
            service,
            f"service_interest mismatch: expected '{service}', got '{message.service_interest}'",
        )
        self.assertEqual(
            message.budget_range,
            test_view_constants.TEST_BUDGET_RANGE_VALUE,
            f"budget_range mismatch: expected '{test_view_constants.TEST_BUDGET_RANGE_VALUE}',"
            f" got '{message.budget_range}'",
        )
        self.assertEqual(
            message.timeline,
            test_view_constants.TEST_TIMELINE_VALUE,
            f"timeline mismatch: expected '{test_view_constants.TEST_TIMELINE_VALUE}', got '{message.timeline}'",
        )

        self.assertEqual(len(mail.outbox), 1, "Expected exactly one email to be sent")
        expected_body = test_view_constants.EMAIL_BODY_WITH_QUALIFICATION_TEMPLATE.format(
            name=test_view_constants.TEST_NAME,
            email=test_view_constants.TEST_EMAIL,
            subject=test_view_constants.TEST_SUBJECT,
            message=test_view_constants.TEST_MESSAGE,
            service_interest_label=test_view_constants.LABEL_SERVICE_INTEREST_TEXT[self.language],
            service_interest=test_view_constants.TEST_SERVICE_TITLE,
            budget_range_label=test_view_constants.LABEL_BUDGET_RANGE_TEXT[self.language],
            budget_range=test_view_constants.TEST_BUDGET_RANGE_DISPLAY[self.language],
            timeline_label=test_view_constants.LABEL_TIMELINE_TEXT[self.language],
            timeline=test_view_constants.TEST_TIMELINE_DISPLAY[self.language],
        )
        self.assertEqual(
            mail.outbox[0].body,
            expected_body,
            f"Email body mismatch: expected\n{expected_body!r}\ngot\n{mail.outbox[0].body!r}",
        )

    def test_qualification_fields_are_optional(self) -> None:
        """Test that omitting qualification fields does not block form submission."""
        form_data = {
            "name": test_view_constants.TEST_NAME,
            "email": test_view_constants.TEST_EMAIL,
            "subject": test_view_constants.TEST_SUBJECT,
            "message": test_view_constants.TEST_MESSAGE,
        }

        response = self.client.post(f"/{self.language}/{self.request_path}", data=form_data)

        self.assertRedirects(
            response,
            f"/{self.language}/{self.request_path}",
            status_code=302,
            target_status_code=200,
        )

        message = ContactMessage.objects.first()
        assert message is not None, "ContactMessage was not created"

        self.assertIsNone(
            message.service_interest,
            f"service_interest should be None when not submitted, got '{message.service_interest}'",
        )
        self.assertEqual(
            message.budget_range,
            "",
            f"budget_range should be empty string when not submitted, got '{message.budget_range}'",
        )
        self.assertEqual(
            message.timeline,
            "",
            f"timeline should be empty string when not submitted, got '{message.timeline}'",
        )


class TestContactViewQualificationFieldsEnglish(BaseTestContactViewQualificationFields):
    """Test qualification fields on the contact form in English."""

    language = Language.ENGLISH


class TestContactViewQualificationFieldsSpanish(BaseTestContactViewQualificationFields):
    """Test qualification fields on the contact form in Spanish."""

    language = Language.SPANISH
