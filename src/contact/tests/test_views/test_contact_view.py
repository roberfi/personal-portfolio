"""Tests for contact view."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

from django.core import mail

import contact.tests.test_views.utils.constants as test_view_constants
from contact.models import ContactMessage
from contact.tests.test_views.base_view_test import BaseContactViewTest
from utils.test_utils.base_view_test_case import ElementText, get_beautiful_soup_from_response
from utils.test_utils.constants import ATTR_PLACEHOLDER, HtmlTag, Language

if TYPE_CHECKING:
    from bs4 import Tag


class BaseTestContactViewContent(BaseContactViewTest):
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
        self.assertEqual(len(mail.outbox), 1)
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
        self.assertEqual(response.status_code, 200)

        # Check no message was saved
        self.assertEqual(ContactMessage.objects.count(), 0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0)

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
        self.assertEqual(response.status_code, 200)

        # Check no message was saved
        self.assertEqual(ContactMessage.objects.count(), 0)

        # Check no email was sent
        self.assertEqual(len(mail.outbox), 0)

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
        self.assertEqual(message.name, test_view_constants.TEST_NAME)
        self.assertEqual(message.email, test_view_constants.TEST_EMAIL)
        self.assertEqual(message.subject, test_view_constants.TEST_SUBJECT)
        self.assertEqual(message.message, test_view_constants.TEST_MESSAGE)
        self.assertFalse(message.is_read)

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
